import asyncio
import subprocess
import click
from aerich import Command

from app.settings import TORTOISE_ORM


@click.group()
def cli():
    """Tortoise-Aerich 数据库迁移管理工具"""
    pass


@cli.command()
@click.argument("cmd")
@click.option("--app", default='aerich')
@click.option('--name', default='auto', help='迁移名字')
def db(cmd, app, name):
    try:
        if cmd == "init":
            async def init_all():
                for k, _ in TORTOISE_ORM["apps"].items():
                    _aerich_cmd = Command(tortoise_config=TORTOISE_ORM, app=k)
                    await _aerich_cmd.init_db(safe=True)
            asyncio.run(init_all())
            click.echo("初始化完成！")
        else:
            match cmd:
                case "migrate":
                    db_cmd_list = ["aerich", "--app", f"{app}", f"{cmd}", "--name", f"{name}"]

                case "upgrade":
                    db_cmd_list = ["aerich", "--app", f"{app}", f"{cmd}"]

                case _:
                    db_cmd_list = ["aerich", f"{cmd}"]

            click.echo(" ".join(db_cmd_list))
            msg = subprocess.check_output(db_cmd_list)
            click.echo(f"操作完成: {msg.decode()}")

    except Exception as e:
        click.echo(f"操作失败: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
