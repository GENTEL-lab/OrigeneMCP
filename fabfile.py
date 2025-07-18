import subprocess as sp
import sys
from pathlib import Path

from fabric import task
from invoke import Context


@task
def run(c: Context):
    """
    运行服务端代码
    """
    sp.check_call(
        "export PYTHONPATH=`fab pypath` ;uv run -m deploy.web",
        cwd=Path(__file__).parent,
        shell=True,
    )


@task
def pypath(c: Context):
    code_root = Path(__file__).parent
    ans = [
        code_root,
        *sys.path,
    ]
    ans = [Path(i).absolute().__str__() for i in ans]
    a = []
    for i in ans:
        if i not in a:
            a.append(i)
    print(":".join(a))
