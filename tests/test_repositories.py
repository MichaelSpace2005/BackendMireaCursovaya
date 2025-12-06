import pytest

from app.entities.mechanic import GameMechanic
from app.entities.link import EvolutionLink


class TestMechanicRepository:
    """Unit tests for MechanicRepository"""

    @pytest.mark.asyncio
    async def test_create_mechanic(self, mechanic_repo, sample_mechanic):
        """Test creating a mechanic"""
        created = await mechanic_repo.create(sample_mechanic)
        
        assert created.id is not None
        assert created.name == sample_mechanic.name
        assert created.description == sample_mechanic.description
        assert created.year == sample_mechanic.year

    @pytest.mark.asyncio
    async def test_get_mechanic_by_id(self, mechanic_repo, created_mechanic):
        """Test getting mechanic by id"""
        retrieved = await mechanic_repo.get_by_id(created_mechanic.id)
        
        assert retrieved is not None
        assert retrieved.id == created_mechanic.id
        assert retrieved.name == created_mechanic.name

    @pytest.mark.asyncio
    async def test_get_nonexistent_mechanic(self, mechanic_repo):
        """Test getting non-existent mechanic returns None"""
        retrieved = await mechanic_repo.get_by_id(9999)
        
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_list_all_mechanics(self, mechanic_repo, created_mechanics):
        """Test listing all mechanics"""
        mechanics = await mechanic_repo.list_all()
        
        assert len(mechanics) >= 2
        assert any(m.id == created_mechanics[0].id for m in mechanics)
        assert any(m.id == created_mechanics[1].id for m in mechanics)

    @pytest.mark.asyncio
    async def test_update_mechanic(self, mechanic_repo, created_mechanic):
        """Test updating a mechanic"""
        updated_mechanic = GameMechanic(
            id=created_mechanic.id,
            name="Updated Combat",
            description="Updated description",
            year=2025
        )
        
        updated = await mechanic_repo.update(updated_mechanic)
        
        assert updated.name == "Updated Combat"
        assert updated.description == "Updated description"
        assert updated.year == 2025

    @pytest.mark.asyncio
    async def test_delete_mechanic(self, mechanic_repo, created_mechanic):
        """Test deleting a mechanic"""
        result = await mechanic_repo.delete(created_mechanic.id)
        
        assert result is True
        
        retrieved = await mechanic_repo.get_by_id(created_mechanic.id)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_mechanic(self, mechanic_repo):
        """Test deleting non-existent mechanic returns False"""
        result = await mechanic_repo.delete(9999)
        
        assert result is False


class TestLinkRepository:
    """Unit tests for LinkRepository"""

    @pytest.mark.asyncio
    async def test_create_link(self, link_repo, created_mechanics):
        """Test creating a link"""
        link = EvolutionLink(
            id=None,
            from_id=created_mechanics[0].id,
            to_id=created_mechanics[1].id,
            type="inheritance"
        )
        
        created = await link_repo.create(link)
        
        assert created.id is not None
        assert created.from_id == link.from_id
        assert created.to_id == link.to_id
        assert created.type == link.type

    @pytest.mark.asyncio
    async def test_get_link_by_id(self, link_repo, created_link):
        """Test getting link by id"""
        retrieved = await link_repo.get_by_id(created_link.id)
        
        assert retrieved is not None
        assert retrieved.id == created_link.id
        assert retrieved.from_id == created_link.from_id
        assert retrieved.to_id == created_link.to_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_link(self, link_repo):
        """Test getting non-existent link returns None"""
        retrieved = await link_repo.get_by_id(9999)
        
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_list_all_links(self, link_repo, created_link):
        """Test listing all links"""
        links = await link_repo.list_all()
        
        assert len(links) >= 1
        assert any(l.id == created_link.id for l in links)

    @pytest.mark.asyncio
    async def test_list_links_by_from_id(self, link_repo, created_link, created_mechanics):
        """Test listing links from specific mechanic"""
        links = await link_repo.list_by_from_id(created_mechanics[0].id)
        
        assert len(links) >= 1
        assert links[0].from_id == created_mechanics[0].id

    @pytest.mark.asyncio
    async def test_delete_link(self, link_repo, created_link):
        """Test deleting a link"""
        result = await link_repo.delete(created_link.id)
        
        assert result is True
        
        retrieved = await link_repo.get_by_id(created_link.id)
        assert retrieved is None


class TestUserRepository:
    """Unit tests for UserRepository"""

    @pytest.mark.asyncio
    async def test_create_user(self, user_repo, sample_user):
        """Test creating a user"""
        created = await user_repo.create(sample_user)
        
        assert created.id is not None
        assert created.email == sample_user.email
        assert created.username == sample_user.username
        assert created.is_verified == sample_user.is_verified

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user_repo, created_user):
        """Test getting user by id"""
        retrieved = await user_repo.get_by_id(created_user.id)
        
        assert retrieved is not None
        assert retrieved.id == created_user.id
        assert retrieved.email == created_user.email

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repo, created_user):
        """Test getting user by email"""
        retrieved = await user_repo.get_by_email(created_user.email)
        
        assert retrieved is not None
        assert retrieved.email == created_user.email

    @pytest.mark.asyncio
    async def test_get_user_by_username(self, user_repo, created_user):
        """Test getting user by username"""
        retrieved = await user_repo.get_by_username(created_user.username)
        
        assert retrieved is not None
        assert retrieved.username == created_user.username

    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, user_repo):
        """Test getting non-existent user returns None"""
        retrieved = await user_repo.get_by_id(9999)
        
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_update_user(self, user_repo, created_user):
        """Test updating a user"""
        from app.entities.user import User
        from datetime import datetime
        
        updated_user = User(
            id=created_user.id,
            email="newemail@example.com",
            username="newusername",
            hashed_password="new_hash",
            is_verified=False,
            created_at=created_user.created_at
        )
        
        updated = await user_repo.update(updated_user)
        
        assert updated.email == "newemail@example.com"
        assert updated.username == "newusername"
        assert updated.is_verified is False
