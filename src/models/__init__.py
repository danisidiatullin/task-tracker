from models.board_models import Board, BoardCreate, BoardRead, BoardReadWithTasks, BoardUpdate



from models.task_models import Task, TaskCreate, TaskRead, \
    TaskReadWithBoard, TaskUpdate







TaskReadWithBoard.update_forward_refs(BoardRead=BoardRead)
BoardReadWithTasks.update_forward_refs(TaskRead=TaskRead)
