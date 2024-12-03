"""
Interactive CLI interface for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint
from typing import Optional, Dict, Any
from datetime import datetime
import os

from src.config import settings
from src.core.file_ops import get_file_info
from src.core.dir_ops import (
    ensure_master_folders,
    analyze_directory,
    organize_files
)
from src.core.drive_ops import (
    get_all_volumes,
    scan_directory,
    build_directory_tree
)

console = Console()

def select_volume() -> Optional[Path]:
    """Interactive volume selection."""
    try:
        volumes = get_all_volumes()
        
        table = Table(title="Available Volumes")
        table.add_column("Index", style="cyan", justify="right")
        table.add_column("Volume", style="green")
        table.add_column("Used", justify="right")
        table.add_column("Free", justify="right")
        table.add_column("Type", style="blue")
        
        for idx, vol in enumerate(volumes, 1):
            used_gb = vol["used"] / (1024**3)
            free_gb = vol["free"] / (1024**3)
            table.add_row(
                str(idx),
                vol["mount_point"],
                f"{used_gb:.1f} GB",
                f"{free_gb:.1f} GB",
                vol["fstype"] or "unknown"
            )
        
        console.print(table)
        
        # Show options
        rprint("\n[cyan]Options:[/cyan]")
        rprint("1-N: Select volume")
        rprint("c: Use current volume")
        rprint("b: Back to main menu")
        rprint("q: Quit program")
        
        choice = Prompt.ask(
            "Select option",
            choices=[str(i) for i in range(1, len(volumes) + 1)] + ['c', 'b', 'q']
        )
        
        if choice == 'q':
            rprint("[cyan]Goodbye![/cyan]")
            exit(0)
        elif choice == 'b':
            return None
        elif choice == 'c':
            return Path.cwd()
        else:
            return Path(volumes[int(choice) - 1]["mount_point"])
            
    except Exception as e:
        rprint(f"[red]Error selecting volume: {str(e)}[/red]")
        return None

def select_directory(start_path: Optional[Path] = None) -> Optional[Path]:
    """Interactive directory selection."""
    try:
        current = start_path or Path.cwd()
        
        while True:
            rprint(f"\n[bold cyan]Current directory:[/bold cyan] {current}")
            
            # Show directory contents
            items = list(current.iterdir())
            dirs = [d for d in items if d.is_dir()]
            
            table = Table()
            table.add_column("Index", style="cyan", justify="right")
            table.add_column("Name", style="green")
            table.add_column("Type", style="blue")
            
            for idx, item in enumerate(dirs, 1):
                table.add_row(str(idx), item.name, "Directory")
            
            console.print(table)
            
            # Show options
            rprint("\n[cyan]Options:[/cyan]")
            rprint("1-N: Select directory")
            rprint("p: Go to parent directory")
            rprint("s: Select current directory")
            rprint("v: Select different volume")
            rprint("b: Back to main menu")
            rprint("q: Quit program")
            
            choice = Prompt.ask(
                "Select option",
                choices=[str(i) for i in range(1, len(dirs) + 1)] + ['p', 's', 'v', 'b', 'q']
            )
            
            if choice == 'q':
                rprint("[cyan]Goodbye![/cyan]")
                exit(0)
            elif choice == 'b':
                return None
            elif choice == 'p':
                current = current.parent
            elif choice == 's':
                return current
            elif choice == 'v':
                vol = select_volume()
                if vol:
                    current = vol
            else:
                current = dirs[int(choice) - 1]
                
    except Exception as e:
        rprint(f"[red]Error selecting directory: {str(e)}[/red]")
        return None

def display_main_menu() -> str:
    """Display main menu and get user choice."""
    # Get current volume
    current_vol = Path.cwd().anchor
    
    menu_options = [
        "List Directory Contents",
        "Analyze Directory",
        "Create Master Folders",
        "Organize Files",
        "Browse Volumes",
        "Search Folders",
        "View Directory Tree",
        "Recent Folders",
        "Compare Directories",
        "Find Duplicates",
        "Git Operations",
        "Manage Master Folders",
        "Change Volume",  # Added option
        "Exit"
    ]
    
    console.print(Panel.fit(
        f"[bold cyan]Enhanced Folder Manager[/bold cyan]\n"
        f"[green]Current Volume: {current_vol}[/green]\n"
        "Organize and manage your files efficiently",
        border_style="blue"
    ))
    
    for idx, option in enumerate(menu_options, 1):
        rprint(f"[cyan]{idx}.[/cyan] {option}")
    
    choice = Prompt.ask(
        "\nSelect an option",
        choices=[str(i) for i in range(1, len(menu_options) + 1)]
    )
    return choice

def list_directory_contents():
    """List contents of selected directory."""
    try:
        path = select_directory()
        if not path:
            return
            
        recursive = Confirm.ask("List contents recursively?")
        show_hidden = Confirm.ask("Show hidden files?")
        
        # Get directory contents
        items = []
        if recursive:
            items.extend(path.rglob("*"))
        else:
            items.extend(path.iterdir())
            
        # Filter hidden files if needed
        if not show_hidden:
            items = [i for i in items if not i.name.startswith('.')]
            
        # Display contents
        table = Table(title=f"Contents of {path}")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Size", style="blue", justify="right")
        table.add_column("Modified", style="magenta")
        
        for item in sorted(items, key=lambda x: (not x.is_dir(), x.name.lower())):
            info = get_file_info(item)
            table.add_row(
                info["name"],
                "Directory" if info["is_dir"] else info["category"],
                f"{info['size']:,} bytes" if not info["is_dir"] else "",
                info["modified"].strftime("%Y-%m-%d %H:%M:%S")
            )
        
        console.print(table)
        
    except Exception as e:
        rprint(f"[red]Error listing directory: {str(e)}[/red]")

def analyze_directory_interactive():
    """Analyze selected directory."""
    try:
        path = select_directory()
        if not path:
            return
            
        stats = analyze_directory(path)
        
        # Print summary
        rprint(f"\n[bold cyan]Analysis of {path}[/bold cyan]")
        rprint(f"Total size: {stats['total_size']:,} bytes")
        rprint(f"Files: {stats['file_count']}")
        rprint(f"Directories: {stats['dir_count']}")
        
        # Show extension statistics
        if stats["extensions"]:
            table = Table(title="File Extensions")
            table.add_column("Extension", style="cyan")
            table.add_column("Count", style="green", justify="right")
            
            for ext, count in sorted(stats["extensions"].items()):
                table.add_row(ext or "(no extension)", str(count))
            
            console.print(table)
            
        # Show category statistics
        if stats["by_category"]:
            table = Table(title="Categories")
            table.add_column("Category", style="cyan")
            table.add_column("Files", style="green", justify="right")
            table.add_column("Total Size", style="blue", justify="right")
            
            for cat, cat_stats in sorted(stats["by_category"].items()):
                table.add_row(
                    cat,
                    str(cat_stats["count"]),
                    f"{cat_stats['total_size']:,} bytes"
                )
            
            console.print(table)
            
    except Exception as e:
        rprint(f"[red]Error analyzing directory: {str(e)}[/red]")

def organize_files_interactive():
    """Organize files in selected directory."""
    try:
        # Select source directory
        rprint("\n[bold cyan]Select source directory:[/bold cyan]")
        source = select_directory()
        if not source:
            return
            
        # Select or create master folder
        master = settings.select_master_folder()
        if not master:
            return
            
        # Confirm operation
        move_files = Confirm.ask("Move files? (No will copy them)")
        
        # Confirm final operation
        if not Confirm.ask(
            f"\nReady to {'move' if move_files else 'copy'} files from {source} to {master}. Continue?"
        ):
            return
            
        # Organize files
        counts = organize_files(source, master, move_files=move_files)
        
        # Show results
        table = Table(title="Organization Results")
        table.add_column("Category", style="cyan")
        table.add_column("Files Processed", style="green", justify="right")
        
        for category, count in counts.items():
            table.add_row(category, str(count))
            
        console.print(table)
        
    except Exception as e:
        rprint(f"[red]Error organizing files: {str(e)}[/red]")

def main():
    """Main program loop."""
    try:
        while True:
            choice = display_main_menu()
            
            if choice == "1":
                list_directory_contents()
            elif choice == "2":
                analyze_directory_interactive()
            elif choice == "3":
                ensure_master_folders()
                rprint("[green]Master folders created successfully![/green]")
            elif choice == "4":
                organize_files_interactive()
            elif choice == "5":
                path = select_volume()
                if path:
                    console.print(build_directory_tree(path))
            elif choice == "6":
                rprint("[yellow]Search feature coming soon...[/yellow]")
            elif choice == "7":
                path = select_directory()
                if path:
                    console.print(build_directory_tree(path))
            elif choice == "8":
                rprint("[yellow]Recent folders feature coming soon...[/yellow]")
            elif choice == "9":
                rprint("[yellow]Compare directories feature coming soon...[/yellow]")
            elif choice == "10":
                rprint("[yellow]Find duplicates feature coming soon...[/yellow]")
            elif choice == "11":
                rprint("[yellow]Git operations feature coming soon...[/yellow]")
            elif choice == "12":
                config = settings.load_config()
                rprint(f"\nMaster folder: {config['master_folder_root']}")
            elif choice == "13":  # Change Volume
                new_vol = select_volume()
                if new_vol and new_vol.exists():
                    try:
                        os.chdir(str(new_vol))
                        rprint(f"[green]Changed to volume: {new_vol}[/green]")
                    except Exception as e:
                        rprint(f"[red]Error changing volume: {str(e)}[/red]")
            elif choice == "14":  # Exit
                rprint("[cyan]Thank you for using Enhanced Folder Manager![/cyan]")
                break
                
            if choice != "14":
                Prompt.ask("\nPress Enter to continue")
                
    except KeyboardInterrupt:
        rprint("\n[cyan]Program terminated by user.[/cyan]")
    except Exception as e:
        rprint(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == '__main__':
    main() 