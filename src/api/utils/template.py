from enum import Enum

from jinja2 import Environment, FileSystemLoader
from sqlalchemy import text

from src.logger import logger


class QueryTemplate(str, Enum):
    count_job_deparment = "count_by_job_deparment.sql"
    count_job_more_mean = "count_job_more_than_mean.sql"


def execute_template_query(session, template_dir, template_name, context: dict):
    env = Environment(loader=FileSystemLoader(template_dir))

    template = env.get_template(template_name)
    sql_query = template.render(context)

    try:
        result = session.execute(text(sql_query))
        rows = result.fetchall()
        return rows
    except Exception as e:
        logger(f"Execution failed {e}")
        return []
