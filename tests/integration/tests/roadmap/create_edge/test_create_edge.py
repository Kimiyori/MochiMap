from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.models.edges.edges import EdgeModel
from src.modules.roadmap.domain.edge.value_objects import EdgeType
from src.modules.roadmap.use_cases.create_edge.command import CreateEdgeCommand


class TestCreateEdge:
    async def make_request(self, client: AsyncClient, roadmap_id: UUID, data: CreateEdgeCommand):
        return await client.post(f"/roadmap/{roadmap_id}/edge", json=data.model_dump(mode="json"))

    @pytest.mark.parametrize("model", [EdgeModel])
    @pytest.mark.usefixtures("check_if_exists")
    async def test_create_edge_success(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes

        r = await self.make_request(
            client,
            roadmap_id,
            CreateEdgeCommand(source_id=str(nodes[0].id), target_id=str(nodes[1].id), type=EdgeType.BEZIER),
        )
        assert r.status_code == status.HTTP_201_CREATED

    async def test_create_edge_duplicate_same_pair_conflict(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes
        node1_id = nodes[0].id
        node2_id = nodes[1].id

        ok = await self.make_request(client, roadmap_id, CreateEdgeCommand(source_id=node1_id, target_id=node2_id))
        assert ok.status_code == status.HTTP_201_CREATED

        dup = await self.make_request(client, roadmap_id, CreateEdgeCommand(source_id=node1_id, target_id=node2_id))
        assert dup.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize("num_nodes", [1])
    async def test_create_edge_missing_nodes_in_roadmap_fails(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes

        bad = await self.make_request(client, roadmap_id, CreateEdgeCommand(source_id=nodes[0].id, target_id=uuid4()))
        assert bad.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("num_nodes", [1])
    async def test_create_edge_self_loop_fails(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes
        node_id = nodes[0].id

        r = await self.make_request(client, roadmap_id, CreateEdgeCommand(source_id=node_id, target_id=node_id))
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    async def test_create_edge_without_type_defaults_to_bezier(
        self,
        client: AsyncClient,
        created_nodes,
        session: AsyncSession,
    ) -> None:
        roadmap_id, nodes = created_nodes

        response = await self.make_request(
            client, roadmap_id, CreateEdgeCommand(source_id=str(nodes[0].id), target_id=str(nodes[1].id))
        )
        assert response.status_code == status.HTTP_201_CREATED
        edge_id: UUID = UUID(response.json()["id"])

        result = await session.execute(select(EdgeModel).where(EdgeModel.id == edge_id))
        edge: EdgeModel | None = result.scalar_one_or_none()
        assert edge is not None
        assert edge.type == EdgeType.BEZIER

    async def test_create_edge_with_type_bezier_persists(
        self,
        client: AsyncClient,
        created_nodes,
        session: AsyncSession,
    ) -> None:
        roadmap_id, nodes = created_nodes
        response = await self.make_request(
            client,
            roadmap_id,
            CreateEdgeCommand(source_id=str(nodes[0].id), target_id=str(nodes[1].id), type=EdgeType.BEZIER),
        )
        assert response.status_code == status.HTTP_201_CREATED
        edge_id: UUID = UUID(response.json()["id"])

        result = await session.execute(select(EdgeModel).where(EdgeModel.id == edge_id))
        edge: EdgeModel | None = result.scalar_one_or_none()
        assert edge is not None
        assert edge.type == EdgeType.BEZIER
