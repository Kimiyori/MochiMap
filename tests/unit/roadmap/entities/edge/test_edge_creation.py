from typing import TYPE_CHECKING

import pytest

from src.modules.roadmap.domain.edge.errors import SelfLoopEdgeError

if TYPE_CHECKING:
    from tests.unit.roadmap.entities.conftest import NodeTestDataFactory, RoadmapTestDataFactory


class TestEdgeCreation:
    def test_create_edge_between_two_nodes(
        self, roadmap_factory: "RoadmapTestDataFactory", node_factory: "NodeTestDataFactory"
    ):
        roadmap = roadmap_factory.create_roadmap()
        n1 = node_factory.create_node(roadmap.id)
        n2 = node_factory.create_node(roadmap.id)
        roadmap.nodes.extend([n1, n2])

        edge = roadmap.create_edge(n1.id, n2.id)

        assert edge in (roadmap.edges or [])
        assert edge.source_id == n1.id
        assert edge.target_id == n2.id
        assert edge.roadmap_id == roadmap.id

    def test_cannot_create_self_loop(
        self, roadmap_factory: "RoadmapTestDataFactory", node_factory: "NodeTestDataFactory"
    ):
        roadmap = roadmap_factory.create_roadmap()
        n1 = node_factory.create_node(roadmap.id)
        roadmap.nodes.append(n1)

        with pytest.raises(SelfLoopEdgeError):
            roadmap.create_edge(n1.id, n1.id)

    def test_allow_duplicate_edge_in_domain_layer(
        self, roadmap_factory: "RoadmapTestDataFactory", node_factory: "NodeTestDataFactory"
    ):
        roadmap = roadmap_factory.create_roadmap()
        n1 = node_factory.create_node(roadmap.id)
        n2 = node_factory.create_node(roadmap.id)

        edge1 = roadmap.create_edge(n1.id, n2.id)
        edge2 = roadmap.create_edge(n1.id, n2.id)

        assert edge1 != edge2
