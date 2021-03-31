from taskmanager.dispatch import TaskManager, SolutionCase, Language, LanguageType
from .AtomicJudge.settings import *

c: str = '''#include <iostream>
using namespace std;
signed main(){
cout<<"Hello, atomic judge!";
return 0;
}'''

if __name__ == '__main__':
    solution = SolutionCase.objects.create(
        code=c,
        language=Language.GNU_CXX_14,
        language_type=LanguageType.COMPILE,
        file_name='main.cpp',
    )
    case = TaskManager(solution=solution)
    case.prepare_env_dir()

