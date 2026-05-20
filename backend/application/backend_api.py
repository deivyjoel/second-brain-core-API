from backend.infrastructure.repositories.image_repository import ImageRepository
from backend.infrastructure.repositories.note_repository import NoteRepository
from backend.infrastructure.repositories.user_repository import UserRepository
from backend.infrastructure.repositories.theme_repository import ThemeRepository
from backend.infrastructure.repositories.analytics_repository import AnalyticsRepository
from backend.infrastructure.repositories.search_efficiency_repository import SearchEfficiencyRepository

from backend.application.use_cases.note_use_cases import (
    create_note, delete_note, get_note_details, get_note_analytics, 
    get_notes_without_themes, list_notes_by_theme, move_to_theme,
    register_time_to_note, rename_note, update_note_content, get_unique_note_name,
    get_note_ids_by_theme_hierarchy, delete_many_notes
)

from backend.application.use_cases.theme_use_cases import (
    create_theme, delete_theme, get_theme_analytics, get_theme_details,
    list_child_themes, list_root_themes, list_themes, remove_theme,
    rename_theme, get_unique_theme_name, get_themes_descendants, delete_many_themes
)

from backend.application.use_cases.image_use_cases import (
    create_image, delete_image, get_image_details, 
    list_images_by_theme, rename_image, move_image_to_theme, get_unique_image_name, delete_many_images,
    list_images_without_theme, get_image_extension, get_image_ids_by_theme_hierarchy
)

from backend.application.use_cases.user_use_cases import (
    login_user, register_user
)
from backend.application.services.image_services import ImageService
from backend.application.services.analyzer_services import AnalyzerService
from backend.application.services.note_services import NoteService
from backend.application.services.theme_services import ThemeService
from backend.application.services.user_services import UserService

class BackendAPI:
    """
    Centralized facade for the frontend.
    Coordinates Repositories and Services to feed Use Cases.
    """

    def __init__(self, note_repo: NoteRepository, 
                theme_repo: ThemeRepository,
                user_repo: UserRepository,
                analy_repo: AnalyticsRepository,
                search_repo: SearchEfficiencyRepository,
                image_repo: ImageRepository):
        # Repositories
        self._note_repo = note_repo
        self._theme_repo = theme_repo
        self._user_repo = user_repo
        self._analy_repo = analy_repo
        self._search_repo = search_repo
        self._image_repo = image_repo

        # Services
        self._analyzer_service = AnalyzerService()
        self._user_service = UserService(self._user_repo)
        self._note_service = NoteService(self._note_repo)
        self._theme_service = ThemeService(self._theme_repo)
        self._image_service = ImageService(self._image_repo)

    # --- User operations ---
    def login_user(self, email: str, password: str):
        return login_user(self._user_repo, email, password, self._user_service)
    
    def register_user(self, name: str, email: str, password: str):
        return register_user(self._user_repo, name, email, password, self._user_service)
    
    # --- Note operations ---
    def create_note(self, user_id: int, name: str, theme_id: int | None = None):
        return create_note(self._note_repo, self._note_service, user_id, name, theme_id)

    def delete_note(self, note_id: int, user_id: int):
        return delete_note(self._note_repo, note_id, user_id)

    def delete_many_notes(self, user_id: int, note_ids: list[int]):
        return delete_many_notes(self._note_repo, user_id, note_ids)

    def rename_note(self, note_id: int, user_id: int, new_name: str):
        return rename_note(self._note_repo, self._note_service, note_id, user_id, new_name)

    def move_note_to_theme(self, note_id: int, user_id: int, new_theme_id: int | None = None):
        return move_to_theme(self._note_repo, self._theme_repo, self._note_service, note_id, user_id, new_theme_id)

    def update_note_content(self, note_id: int, user_id: int, content: str):
        return update_note_content(self._note_repo, note_id, user_id, content)

    def get_note_details(self, note_id: int, user_id: int):
        return get_note_details(self._note_repo, note_id, user_id)

    def get_note_analytics(self, note_id: int, user_id: int):
        return get_note_analytics(self._note_repo, self._analyzer_service, note_id, user_id)

    def list_notes_by_theme(self, theme_id: int, user_id: int):
        return list_notes_by_theme(self._note_repo, self._theme_repo, theme_id, user_id)

    def get_notes_without_themes(self, user_id: int):
        return get_notes_without_themes(self._note_repo, user_id)

    def register_time_to_note(self, note_id: int, user_id: int, minutes: float):
        return register_time_to_note(self._note_repo, minutes, note_id, user_id)

    def get_unique_note_name(self, user_id: int, name: str, theme_id: int | None = None):
        return get_unique_note_name(self._theme_repo, self._note_service, user_id, name, theme_id)

    def get_note_ids_by_theme_hierarchy(self, theme_id: int, user_id: int):
        return get_note_ids_by_theme_hierarchy(self._search_repo, theme_id, user_id)

    # --- Theme operations ---
    def create_theme(self, user_id: int, name: str, parent_id: int | None = None):
        return create_theme(self._theme_repo, self._theme_service, user_id, name, parent_id)

    def delete_theme(self, theme_id: int, user_id: int):
        return delete_theme(self._theme_repo, theme_id, user_id)
    
    def delete_many_themes(self, user_id: int, theme_ids: list[int]):
        return delete_many_themes(self._theme_repo, user_id, theme_ids)

    def rename_theme(self, theme_id: int, user_id: int, new_name: str):
        return rename_theme(self._theme_repo, self._theme_service, theme_id, user_id, new_name)

    def move_theme(self, theme_id: int, user_id: int, new_parent_id: int | None = None):
        return remove_theme(self._theme_repo, self._search_repo, self._theme_service, theme_id, user_id, new_parent_id)

    def get_unique_theme_name(self, user_id: int, name: str, theme_id: int | None = None):
        return get_unique_theme_name(self._theme_repo, self._theme_service, user_id, name, theme_id)

    def list_themes(self, user_id: int):
        return list_themes(self._theme_repo, user_id)

    def list_root_themes(self, user_id: int):
        return list_root_themes(self._theme_repo, user_id)

    def list_child_themes(self, parent_id: int, user_id: int):
        return list_child_themes(self._theme_repo, user_id, parent_id)

    def get_theme_details(self, theme_id: int, user_id: int):
        return get_theme_details(self._theme_repo, theme_id, user_id)

    def get_theme_analytics(self, theme_id: int, user_id: int):
        return get_theme_analytics(
            self._analy_repo,
            self._search_repo,
            self._theme_repo,
            self._analyzer_service,
            theme_id,
            user_id
        )

    def get_themes_descendants(self, theme_id: int, user_id: int):
        return get_themes_descendants(self._search_repo, theme_id, user_id)
    
    # --- Image operations ---
    def create_image(self, user_id: int, name: str, blob_data: bytes, extension: str, theme_id: int | None = None):
        return create_image(self._image_repo, self._image_service, user_id, name, blob_data, extension, theme_id)

    def delete_image(self, image_id: int, user_id: int):
        return delete_image(self._image_repo, image_id, user_id)

    def delete_many_images(self, user_id: int, image_ids: list[int]):
        return delete_many_images(self._image_repo, user_id, image_ids)

    def rename_image(self, image_id: int, user_id: int, new_name: str):
        return rename_image(self._image_repo, self._image_service, image_id, user_id, new_name)

    def move_image_to_theme(self, image_id: int, user_id: int, new_theme_id: int | None = None):
        return move_image_to_theme(self._image_repo, self._theme_repo, self._image_service, image_id, user_id, new_theme_id)

    def get_image_details(self, image_id: int, user_id: int):
        return get_image_details(self._image_repo, image_id, user_id)

    def list_images_by_theme(self, theme_id: int, user_id: int):
        return list_images_by_theme(self._image_repo, self._theme_repo, theme_id, user_id)

    def get_images_without_theme(self, user_id: int):
        return list_images_without_theme(self._image_repo, user_id)

    def get_unique_image_name(self, user_id: int, name: str, theme_id: int | None = None):
        return get_unique_image_name(self._theme_repo, self._image_service, user_id, name, theme_id)

    def get_image_extension(self, image_id: int, user_id: int):
        return get_image_extension(self._image_repo, image_id, user_id)
    
    def get_image_ids_by_theme_hierarchy(self, theme_id: int, user_id: int):
        return get_image_ids_by_theme_hierarchy(self._search_repo, theme_id, user_id)