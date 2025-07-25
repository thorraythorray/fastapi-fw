import asyncio
import subprocess

import click
from aerich import Command

from app.core.config import TORTOISE_ORM


@click.group()
def cli():
    """管理工具"""
    pass


@cli.command()
def lint():
    """代码风格检查（可选自动修复）"""
    # if fix:
    #     subprocess.call("autopep8 --in-place --recursive app/", shell=True)
    subprocess.call("pycodestyle --config=.tox.ini app/", shell=True)
    subprocess.call("pylint --rcfile=.pylintrc app/", shell=True)


@cli.command()
@click.argument("cmd")
@click.option("--app", default='aerich')
@click.option('--name', default='auto', help='迁移名字')
def db(cmd, app, name):
    """数据库迁移和管理命令封装"""
    valid_cmds = {"init", "migrate", "upgrade", "downgrade", "history", "heads", "current", "revision"}
    try:
        if cmd == "init":
            async def init_all():
                for k, _ in TORTOISE_ORM["apps"].items():
                    _aerich_cmd = Command(tortoise_config=TORTOISE_ORM, app=k)
                    await _aerich_cmd.init_db(safe=True)
            asyncio.run(init_all())
            click.echo("初始化完成！")
        else:
            if cmd not in valid_cmds:
                click.echo(f"不支持的命令: {cmd}")
                return
            if cmd == "migrate":
                db_cmd_list = ["aerich", "--app", f"{app}", f"{cmd}", "--name", f"{name}"]
            elif cmd == "upgrade":
                db_cmd_list = ["aerich", "--app", f"{app}", f"{cmd}"]
            else:
                db_cmd_list = ["aerich", f"{cmd}"]
            click.echo(" ".join(db_cmd_list))
            msg = subprocess.check_output(db_cmd_list, stderr=subprocess.STDOUT)
            click.echo(f"操作完成: {msg.decode()}")
    except subprocess.CalledProcessError as e:
        click.echo(f"子进程错误: {e.output.decode()}", err=True)
    except Exception as e:
        click.echo(f"操作失败: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
