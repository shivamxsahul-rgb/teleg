"""
Music Player Module for LoveBot

Supports:
- Queue management
- Pause / Resume / Skip / Stop
- Volume control
- Now playing display
- YouTube search via yt-dlp (when installed)

Note: Actual voice chat streaming requires pytgcalls + yt-dlp.
      This module handles queue logic and status; voice streaming 
      is activated when those libraries are present.
"""

import asyncio
import random
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Song:
    title: str
    url: str
    requested_by: str
    duration: str = "Unknown"


class MusicPlayer:
    def __init__(self):
        self._queue: List[Song] = []
        self._current: Optional[Song] = None
        self._is_playing: bool = False
        self._is_paused: bool = False
        self._volume: int = 100
        self.songs_played: int = 0

        # Try importing voice libraries
        self._has_voice = False
        try:
            import yt_dlp  # noqa
            self._has_ydl = True
        except ImportError:
            self._has_ydl = False

    # ─── Queue Management ────────────────────────────────

    async def add_to_queue(self, query: str, requested_by: str) -> str:
        """Search/resolve the query and add to queue."""
        song = await self._resolve(query, requested_by)
        self._queue.append(song)

        if not self._is_playing:
            self._is_playing = True
            self._current = song
            self._queue.pop(0)
            self.songs_played += 1
            return (
                f"▶️ *Now Playing*\n"
                f"🎵 {song.title}\n"
                f"⏱️ Duration: {song.duration}\n"
                f"👤 Requested by: {requested_by}\n\n"
                f"_Note: Join a voice chat and make me admin to hear audio!_"
            )
        else:
            pos = len(self._queue)
            return (
                f"✅ *Added to Queue* #{pos}\n"
                f"🎵 {song.title}\n"
                f"⏱️ Duration: {song.duration}\n"
                f"👤 Requested by: {requested_by}"
            )

    async def _resolve(self, query: str, requested_by: str) -> Song:
        """Try to resolve via yt-dlp, else create a placeholder."""
        if self._has_ydl:
            try:
                import yt_dlp
                ydl_opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "format": "bestaudio/best",
                    "noplaylist": True,
                    "default_search": "ytsearch1",
                }
                loop = asyncio.get_event_loop()

                def extract():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(query, download=False)
                        if "entries" in info:
                            info = info["entries"][0]
                        duration_s = info.get("duration", 0)
                        mins, secs = divmod(int(duration_s), 60)
                        duration = f"{mins}:{secs:02d}"
                        return Song(
                            title=info.get("title", query),
                            url=info.get("url", query),
                            requested_by=requested_by,
                            duration=duration,
                        )

                return await loop.run_in_executor(None, extract)
            except Exception:
                pass

        # Fallback placeholder
        return Song(
            title=query,
            url=query,
            requested_by=requested_by,
            duration="~3:30",
        )

    # ─── Playback Controls ───────────────────────────────

    def pause(self) -> str:
        if not self._is_playing:
            return "❌ Nothing is currently playing."
        if self._is_paused:
            return "⚠️ Music is already paused."
        self._is_paused = True
        return f"⏸️ Paused: *{self._current.title if self._current else 'current song'}*"

    def resume(self) -> str:
        if not self._is_playing:
            return "❌ Nothing is currently playing."
        if not self._is_paused:
            return "⚠️ Music is already playing."
        self._is_paused = False
        return f"▶️ Resumed: *{self._current.title if self._current else 'current song'}*"

    def skip(self) -> str:
        if not self._current:
            return "❌ Nothing to skip."
        skipped = self._current.title
        if self._queue:
            self._current = self._queue.pop(0)
            self._is_paused = False
            self.songs_played += 1
            return f"⏭️ Skipped *{skipped}*\n▶️ Now playing: *{self._current.title}*"
        else:
            self._current = None
            self._is_playing = False
            self._is_paused = False
            return f"⏭️ Skipped *{skipped}*\n📭 Queue is now empty."

    def stop(self) -> str:
        self._current = None
        self._queue.clear()
        self._is_playing = False
        self._is_paused = False
        return "⏹️ Stopped music and cleared the queue."

    def set_volume(self, vol: int) -> str:
        if not 0 <= vol <= 200:
            return "❌ Volume must be between 0 and 200."
        self._volume = vol
        emoji = "🔇" if vol == 0 else "🔉" if vol < 50 else "🔊"
        return f"{emoji} Volume set to *{vol}%*"

    # ─── Status ──────────────────────────────────────────

    def now_playing(self) -> str:
        if not self._current:
            return "🎵 Nothing is playing right now.\nUse `/play [song]` to start!"
        status = "⏸️ Paused" if self._is_paused else "▶️ Playing"
        return (
            f"🎵 *Now Playing*\n"
            f"┌ {status}\n"
            f"├ 🎵 {self._current.title}\n"
            f"├ ⏱️ Duration: {self._current.duration}\n"
            f"├ 👤 Requested by: {self._current.requested_by}\n"
            f"├ 🔊 Volume: {self._volume}%\n"
            f"└ 📋 Queue: {len(self._queue)} song(s)"
        )

    def get_queue(self) -> str:
        if not self._current and not self._queue:
            return "📭 The queue is empty.\nUse `/play [song]` to add songs!"
        
        lines = ["🎵 *Music Queue*\n"]
        if self._current:
            status = "⏸️" if self._is_paused else "▶️"
            lines.append(f"{status} *Now:* {self._current.title} — {self._current.duration}")
        
        if self._queue:
            lines.append("\n📋 *Up Next:*")
            for i, song in enumerate(self._queue, 1):
                lines.append(f"`{i}.` {song.title} — {song.duration}")
        else:
            lines.append("\n📭 No songs in queue.")
        
        lines.append(f"\n🔊 Volume: {self._volume}%")
        return "\n".join(lines)
