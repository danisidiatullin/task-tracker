from models.board import Board, BoardCreate, BoardRead, BoardReadWithTasks, BoardUpdate
from models.task import Task, TaskCreate, TaskRead, TaskReadWithBoard, TaskUpdate
from models.user import User, UserCreate, UserRead

TaskReadWithBoard.update_forward_refs(BoardRead=BoardRead)
BoardReadWithTasks.update_forward_refs(TaskRead=TaskRead)
UserRead.update_forward_refs(TaskRead=TaskRead)
