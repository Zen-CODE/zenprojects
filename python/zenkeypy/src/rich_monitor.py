import time
from textwrap import dedent

from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table


def create_layout() -> Layout:
    """Create the structural layout for the music player UI."""
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )

    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    return layout

def generate_dashboard(song_title, artist, current_sec, total_sec, playlist, volume):
    """Generates the updated renderable content for the Live display."""
    layout = create_layout()

    layout["header"].update(
        Panel("[bold blue]♪ ZenKeyPy MPD Audio Monitor ♪[/bold blue]")
    )

    progress_bar = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.completed}/{task.total}s"),
    )
    progress_bar.add_task("Playing", completed=current_sec, total=total_sec)

    info_text = dedent(f"""
        [bold cyan]Title:[/bold cyan] {song_title}
        [bold cyan]Artist:[/bold cyan] {artist}
        [bold cyan]Volume:[/bold cyan] {volume}%
        """)

    left_content = Group(info_text, progress_bar)
    layout["left"].update(Panel(left_content, title="Now Playing", border_style="green"))

    queue_table = Table(show_header=True, header_style="bold blue", expand=True)
    queue_table.add_column("#", width=3)
    queue_table.add_column("Track")

    for idx, track in enumerate(playlist, 1):
        if track == song_title:
            queue_table.add_row(str(idx), f"[bold green]▶ {track}[/bold green]")
        else:
            queue_table.add_row(str(idx), track)

    layout["right"].update(Panel(queue_table, title="Queue", border_style="blue"))

    return layout

if __name__ == "__main__":
    playlist = ["Bohemian Rhapsody", "Stairway to Heaven", "Hotel California", "Imagine", "Billie Jean"]
    current_song_idx = 0
    duration = 30  # Simulated song duration in seconds
    elapsed = 0
    volume = 80

    # Using Rich's Live display to dynamically update the screen in place
    with Live(refresh_per_second=4, screen=False) as live:
        try:
            while True:
                song = playlist[current_song_idx]

                # Update dashboard view
                renderable = generate_dashboard(
                    song_title=song,
                    artist="Classic Rock Icons",
                    current_sec=elapsed,
                    total_sec=duration,
                    playlist=playlist,
                    volume=volume
                )
                live.update(renderable)

                # Simulate playback progression
                time.sleep(1)
                elapsed += 1

        except KeyboardInterrupt:
            pass
