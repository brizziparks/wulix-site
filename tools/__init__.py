from .web_search import search_web
from .memory_tool import remember, recall, forget, load_memory
from .system_tools import (
    open_application, open_url,
    volume_up, volume_down, volume_mute_toggle,
    youtube_search_play, open_youtube_url,
)
from .file_tools import read_file, write_file, list_files
from .datetime_tool import get_datetime
from .notify import notify, remind
from .system_advanced import (
    get_clipboard, set_clipboard,
    take_screenshot,
    set_volume, mute,
)
from .outlook import (
    get_unread_emails, search_emails, send_email, draft_email,
    get_calendar_today, get_calendar_range, create_meeting,
)
from .gmail import (
    gmail_unread, gmail_search, gmail_send,
    gcal_today, gcal_range, gcal_create,
)
from .n8n_tool import trigger_webhook, list_workflows, activate_workflow
from .clipboard_history import (
    get_clipboard_history, get_last_clipboard,
    restore_clipboard, clear_clipboard_history,
    start_clipboard_watcher,
)
from .file_watcher import start_watching, stop_watching, get_recent_files, list_watchers
from .ocr_screen import extract_text_from_screen, extract_text_from_image, find_text_on_screen
from .google_workspace import (
    create_doc, append_to_doc, read_doc,
    create_sheet, append_to_sheet, read_sheet,
    list_drive_files,
)

__all__ = [
    "search_web",
    "remember", "recall", "forget", "load_memory",
    "open_application", "open_url",
    "volume_up", "volume_down", "volume_mute_toggle",
    "youtube_search_play", "open_youtube_url",
    "read_file", "write_file", "list_files",
    "get_datetime",
    "notify", "remind",
    "get_clipboard", "set_clipboard",
    "take_screenshot",
    "set_volume", "mute",
    # Outlook
    "get_unread_emails", "search_emails", "send_email", "draft_email",
    "get_calendar_today", "get_calendar_range", "create_meeting",
    # Gmail + Google Calendar
    "gmail_unread", "gmail_search", "gmail_send",
    "gcal_today", "gcal_range", "gcal_create",
    # N8n
    "trigger_webhook", "list_workflows", "activate_workflow",
    # Clipboard history
    "get_clipboard_history", "get_last_clipboard",
    "restore_clipboard", "clear_clipboard_history", "start_clipboard_watcher",
    # File watcher
    "start_watching", "stop_watching", "get_recent_files", "list_watchers",
    # OCR
    "extract_text_from_screen", "extract_text_from_image", "find_text_on_screen",
    # Google Workspace
    "create_doc", "append_to_doc", "read_doc",
    "create_sheet", "append_to_sheet", "read_sheet", "list_drive_files",
]
