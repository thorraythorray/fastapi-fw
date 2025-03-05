import asyncio
import subprocess
import time

import click
from aerich import Command

from app.config import TORTOISE_ORM


@click.group()
def cli():
    """管理工具"""
    pass


@cli.command()
def lint():
    subprocess.call("pycodestyle --config=.tox.ini .", shell=True)
    time.sleep(0.2)
    subprocess.call("pylint --rcfile=.pylintrc app/auth", shell=True)


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
            if cmd == "migrate":
                db_cmd_list = ["aerich", "--app", f"{app}", f"{cmd}", "--name", f"{name}"]
            elif cmd == "upgrade":
                db_cmd_list = ["aerich", "--app", f"{app}", f"{cmd}"]
            else:
                db_cmd_list = ["aerich", f"{cmd}"]

            click.echo(" ".join(db_cmd_list))
            msg = subprocess.check_output(db_cmd_list)
            click.echo(f"操作完成: {msg.decode()}")

    except Exception as e:
        click.echo(f"操作失败: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
