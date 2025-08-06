from typing import TYPE_CHECKING

from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import Position
from src.modules.roadmap.use_cases.move_node.command import MoveNodeCommand, PositionDTO

if TYPE_CHECKING:
    from faker import Faker


class TestNodeMove:
    def test_move_learning_node(self, learning_note_node: Node, fake: "Faker"):

        updated_x = fake.pyfloat(min_value=50, max_value=100)
        updated_y = fake.pyfloat(min_value=50, max_value=100)

        move_cmd = MoveNodeCommand(
            position=PositionDTO(x=updated_x, y=updated_y),
        )

        learning_note_node.move_node(move_cmd)

        assert learning_note_node.position == Position(x=updated_x, y=updated_y)

    def test_move_resource_node(self, resource_bookmark_node: Node, fake: "Faker"):

        updated_x = fake.pyfloat(min_value=50, max_value=100)
        updated_y = fake.pyfloat(min_value=50, max_value=100)

        move_cmd = MoveNodeCommand(
            position=PositionDTO(x=updated_x, y=updated_y),
        )

        resource_bookmark_node.move_node(move_cmd)

        assert resource_bookmark_node.position == Position(x=updated_x, y=updated_y)