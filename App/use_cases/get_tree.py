from typing import Protocol, List, Dict, Any
from app.entities.mechanic import GameMechanic
from app.entities.link import EvolutionLink

class IMechanicRepo(Protocol):
    async def get_by_id(self, id: int) -> GameMechanic | None: ...
    async def list_all(self) -> List[GameMechanic]: ...

class ILinkRepo(Protocol):
    async def list_links_from(self, from_id: int) -> List[EvolutionLink]: ...
    async def list_links(self) -> List[EvolutionLink]: ...

class GetMechanicTreeUseCase:
    def __init__(self, mechanic_repo: IMechanicRepo, link_repo: ILinkRepo):
        self.mechanic_repo = mechanic_repo
        self.link_repo = link_repo

    async def execute(self, root_id: int) -> Dict[str, Any]:
        root = await self.mechanic_repo.get_by_id(root_id)
        if not root:
            raise ValueError("Root mechanic not found")

        # load all links and mechanics (for simplicity)
        links = await self.link_repo.list_links()
        mechanics = {m.id: m for m in await self.mechanic_repo.list_all()}

        # build adjacency
        children_map: dict[int, list] = {}
        for link in links:
            children_map.setdefault(link.from_id, []).append(link)

        def build_node(mid: int, visited: set) -> dict:
            if mid in visited:
                return {"id": mid, "name": mechanics[mid].name, "cycle": True}
            visited.add(mid)
            node = {
                "id": mid,
                "name": mechanics[mid].name,
                "description": mechanics[mid].description,
                "year": mechanics[mid].year,
                "children": []
            }
            for l in children_map.get(mid, []):
                if l.to_id in mechanics:
                    node["children"].append({
                        "type": l.type,
                        "node": build_node(l.to_id, visited.copy())
                    })
            return node

        tree = build_node(root.id, set())
        return {"root": tree}