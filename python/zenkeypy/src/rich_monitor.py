import time
from textwrap import dedent

from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from mpd import MPDClient


class ZenMPDClient:

    def __init__(self):
        self.client = MPDClient()
        self.client.connect("localhost", 6600)

    def close(self):
        try:
            self.client.close()
            self.client.disconnect()
        except Exception as e:  # NOQA: BLE001
            print(f"Error closing MPDClient: {e}")


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

def generate_dashboard(current_song: dict):
    """Generates the updated renderable content for the Live display."""
    # ------ Current song keys -------
    # {'file': 'Wumpscut/Blutkind - Disc 2/06 - Throbberstalk.mp3',
    # 'last-modified': '2023-02-22T05:20:28Z', 'format': '44100:24:2',
    # 'artist': 'Wumpscut', 'title': 'Throbberstalk',
    # 'album': 'Blutkind - Disc 2', 'track': '6', 'date': '2000',
    # 'genre': 'Industrial', 'time': '258', 'duration': '258.272',
    # 'pos': '5', 'id': '1055'}

    layout = create_layout()

    layout["header"].update(
        Panel("[bold blue]♪ ZenKeyPy MPD Audio Monitor ♪[/bold blue]")
    )

    progress_bar = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.completed}/{task.total}s"),
    )
    progress_bar.add_task("Playing",
                          completed=float(current_song.get("time", 0)),
                          total=float(current_song.get("duration", 1)))

    info_text = dedent(f"""
        [bold cyan]Artist:[/bold cyan] {current_song.get("artist", "")}
        [bold cyan]Albumn:[/bold cyan] {current_song.get("album", "")}
        [bold cyan]Title:[/bold cyan] {current_song.get("title", "")}
        [bold cyan]File:[/bold cyan] {current_song.get("file", "")}
        """)

    left_content = Group(info_text, progress_bar)
    layout["left"].update(Panel(left_content, title="Now Playing", border_style="green"))

    queue_table = Table(show_header=True, header_style="bold blue", expand=True)
    queue_table.add_column("#", width=3)
    queue_table.add_column("Track")

    # for idx, track in enumerate(playlist, 1):
    #     if track == song_title:
    #         queue_table.add_row(str(idx), f"[bold green]▶ {track}[/bold green]")
    #     else:
    #         queue_table.add_row(str(idx), track)

    layout["right"].update(Panel(queue_table, title="Queue", border_style="blue"))

    return layout

if __name__ == "__main__":
    zen_mpd: ZenMPDClient = ZenMPDClient()

    # Using Rich's Live display to dynamically update the screen in place
    with Live(refresh_per_second=4, screen=False) as live:
        try:

            while True:
                current_song: dict = zen_mpd.client.currentsong()

                # Update dashboard view
                renderable = generate_dashboard(current_song=current_song)
                live.update(renderable)

                # Simulate playback progression
                time.sleep(1)

        except KeyboardInterrupt:
            print("Exiting...")
            zen_mpd.close()
