import pytest
from datetime import datetime, timedelta

from app.use_cases.create_mechanic import CreateMechanicUseCase
from app.use_cases.get_tree import GetMechanicTreeUseCase
from app.entities.mechanic import GameMechanic


class TestCreateMechanicUseCase:
    """Unit tests for CreateMechanicUseCase"""

    @pytest.mark.asyncio
    async def test_create_mechanic_success(self, mechanic_repo):
        """Test successful mechanic creation"""
        use_case = CreateMechanicUseCase(mechanic_repo)
        
        mechanic = GameMechanic(
            id=None,
            name="New Mechanic",
            description="Test mechanic",
            year=2024
        )
        
        result = await use_case.execute(mechanic)
        
        assert result.id is not None
        assert result.name == "New Mechanic"

    @pytest.mark.asyncio
    async def test_create_mechanic_with_empty_name_fails(self, mechanic_repo):
        """Test that mechanic with empty name fails"""
        use_case = CreateMechanicUseCase(mechanic_repo)
        
        mechanic = GameMechanic(
            id=None,
            name="",
            description="Test mechanic",
            year=2024
        )
        
        with pytest.raises(ValueError, match="Mechanic name cannot be empty"):
            await use_case.execute(mechanic)

    @pytest.mark.asyncio
    async def test_create_mechanic_with_whitespace_name_fails(self, mechanic_repo):
        """Test that mechanic with whitespace-only name fails"""
        use_case = CreateMechanicUseCase(mechanic_repo)
        
        mechanic = GameMechanic(
            id=None,
            name="   ",
            description="Test mechanic",
            year=2024
        )
        
        with pytest.raises(ValueError, match="Mechanic name cannot be empty"):
            await use_case.execute(mechanic)


class TestGetMechanicTreeUseCase:
    """Unit tests for GetMechanicTreeUseCase"""

    @pytest.mark.asyncio
    async def test_get_tree_single_mechanic(self, mechanic_repo, link_repo, created_mechanic):
        """Test getting tree for single mechanic with no links"""
        use_case = GetMechanicTreeUseCase(mechanic_repo, link_repo)
        
        tree = await use_case.execute(created_mechanic.id)
        
        assert tree.mechanic.id == created_mechanic.id
        assert len(tree.children) == 0

    @pytest.mark.asyncio
    async def test_get_tree_with_children(self, mechanic_repo, link_repo, test_db_session):
        """Test getting tree with child mechanics"""
        # Create mechanics
        m1 = GameMechanic(id=None, name="Parent", description="", year=2024)
        m2 = GameMechanic(id=None, name="Child1", description="", year=2024)
        m3 = GameMechanic(id=None, name="Child2", description="", year=2024)
        
        created_m1 = await mechanic_repo.create(m1)
        created_m2 = await mechanic_repo.create(m2)
        created_m3 = await mechanic_repo.create(m3)
        
        # Create links
        from app.entities.link import EvolutionLink
        link1 = EvolutionLink(
            id=None,
            from_id=created_m1.id,
            to_id=created_m2.id,
            type="inheritance"
        )
        link2 = EvolutionLink(
            id=None,
            from_id=created_m1.id,
            to_id=created_m3.id,
            type="composition"
        )
        
        await link_repo.create(link1)
        await link_repo.create(link2)
        
        use_case = GetMechanicTreeUseCase(mechanic_repo, link_repo)
        tree = await use_case.execute(created_m1.id)
        
        assert tree.mechanic.id == created_m1.id
        assert len(tree.children) == 2

    @pytest.mark.asyncio
    async def test_get_tree_detects_cycles(self, mechanic_repo, link_repo):
        """Test that tree building detects cycles"""
        # Create mechanics
        m1 = GameMechanic(id=None, name="M1", description="", year=2024)
        m2 = GameMechanic(id=None, name="M2", description="", year=2024)
        m3 = GameMechanic(id=None, name="M3", description="", year=2024)
        
        created_m1 = await mechanic_repo.create(m1)
        created_m2 = await mechanic_repo.create(m2)
        created_m3 = await mechanic_repo.create(m3)
        
        # Create cycle: M1 -> M2 -> M3 -> M1
        from app.entities.link import EvolutionLink
        link1 = EvolutionLink(id=None, from_id=created_m1.id, to_id=created_m2.id, type="inheritance")
        link2 = EvolutionLink(id=None, from_id=created_m2.id, to_id=created_m3.id, type="inheritance")
        link3 = EvolutionLink(id=None, from_id=created_m3.id, to_id=created_m1.id, type="inheritance")
        
        await link_repo.create(link1)
        await link_repo.create(link2)
        await link_repo.create(link3)
        
        use_case = GetMechanicTreeUseCase(mechanic_repo, link_repo)
        
        # Should not raise error, should just stop recursing
        tree = await use_case.execute(created_m1.id)
        assert tree.mechanic.id == created_m1.id

    @pytest.mark.asyncio
    async def test_get_tree_nonexistent_mechanic(self, mechanic_repo, link_repo):
        """Test getting tree for non-existent mechanic"""
        use_case = GetMechanicTreeUseCase(mechanic_repo, link_repo)
        
        with pytest.raises(ValueError, match="Mechanic not found"):
            await use_case.execute(9999)
