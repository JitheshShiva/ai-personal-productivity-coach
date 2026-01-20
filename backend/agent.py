from dotenv import load_dotenv
load_dotenv()

from pydantic_ai import Agent
from backend.models import ProductivityInput, ProductivityPlan


agent = Agent(
    model="openrouter:mistralai/mistral-7b-instruct",
    system_prompt="""
You are an AI personal productivity coach.

You MUST follow these rules:
1. Start the schedule from the provided start_time.
2. Split available_hours across all tasks.
3. Each task must have start_time and end_time in HH:MM format.
4. Do not leave the schedule empty.

Energy level handling:
- High energy:
  • Longer deep-focus work blocks
  • Fewer breaks
- Medium energy:
  • Balanced work blocks
- Low energy:
  • Shorter tasks
  • Gentle pacing and breaks

Be practical, clear, and motivating.
""",
    retries=2
)


async def run_productivity_agent(user_input: ProductivityInput):
    try:
        # ---------- AI-generated plan ----------
        result = await agent.run(
            user_input,
            result_type=ProductivityPlan
        )

        plan = result.data

        # ---------- Energy-based post-processing ----------
        if user_input.energy_level == "high":
            plan.tips.append("Use your high energy for deep, focused work")
        elif user_input.energy_level == "low":
            plan.tips.append("Keep tasks light and take regular breaks")
        else:
            plan.tips.append("Maintain a steady and balanced workflow")

        return plan

    except Exception:
        # ---------- Deterministic fallback ----------
        schedule = []

        # Parse exact start time (HH:MM)
        start_hour, start_minute = map(int, user_input.start_time.split(":"))
        current_minutes = start_hour * 60 + start_minute

        task_count = max(len(user_input.goals), 1)

        # Energy-based task duration
        if user_input.energy_level == "high":
            minutes_per_task = int((user_input.available_hours * 60) / task_count)
        elif user_input.energy_level == "low":
            minutes_per_task = int((user_input.available_hours * 60) / (task_count + 1))
        else:
            minutes_per_task = int((user_input.available_hours * 60) / task_count)

        for task in user_input.goals:
            start_time = f"{current_minutes // 60:02d}:{current_minutes % 60:02d}"
            end_minutes = current_minutes + minutes_per_task
            end_time = f"{end_minutes // 60:02d}:{end_minutes % 60:02d}"

            schedule.append({
                "task": task,
                "start_time": start_time,
                "end_time": end_time
            })

            current_minutes = end_minutes

        # ---------- Energy-aware tips ----------
        tips = ["Focus on one task at a time"]

        if user_input.energy_level == "high":
            tips.append("Use your high energy for deep, focused work")
        elif user_input.energy_level == "low":
            tips.append("Keep tasks light and avoid burnout")
        else:
            tips.append("Maintain a steady and balanced workflow")

        return ProductivityPlan(
            priority_order=user_input.goals,
            schedule=schedule,
            tips=tips
        )
