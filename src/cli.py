"""
Command line interface for OpenDocGen.
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

from .main import create_app
from .config import get_settings, create_directories

app = typer.Typer(
    name="opendocgen",
    help="Open-source autonomous document generation agent",
    add_completion=False,
)
console = Console()


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
    workers: int = typer.Option(1, help="Number of worker processes"),
    log_level: str = typer.Option("info", help="Log level"),
):
    """Start the OpenDocGen server."""
    import uvicorn
    
    settings = get_settings()
    
    console.print(f"🚀 Starting OpenDocGen v{settings.app_version}", style="bold blue")
    console.print(f"📍 Server: http://{host}:{port}", style="bold green")
    console.print(f"📚 API Docs: http://{host}:{port}/docs", style="bold green")
    
    # Create necessary directories
    create_directories()
    
    # Start server
    uvicorn.run(
        "src.cli:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
        log_level=log_level.lower(),
    )


@app.command()
def generate(
    topic: str = typer.Argument(..., help="Topic for document generation"),
    output: Optional[Path] = typer.Option(None, help="Output file path"),
    template: str = typer.Option("research_paper", help="Document template"),
    model: str = typer.Option("llama2", help="LLM model to use"),
):
    """Generate a document from a topic."""
    console.print(f"📝 Generating document for topic: {topic}", style="bold blue")
    
    # TODO: Implement document generation logic
    console.print("⚠️  Document generation not yet implemented", style="bold yellow")


@app.command()
def setup(
    force: bool = typer.Option(False, help="Force recreate directories"),
):
    """Setup OpenDocGen environment."""
    console.print("🔧 Setting up OpenDocGen environment...", style="bold blue")
    
    # Create directories
    create_directories()
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        console.print("✅ Created .env file from .env.example", style="bold green")
    
    console.print("✅ Setup complete!", style="bold green")


@app.command()
def version():
    """Show version information."""
    settings = get_settings()
    console.print(f"OpenDocGen v{settings.app_version}", style="bold blue")


@app.command()
def config(
    show: bool = typer.Option(False, help="Show current configuration"),
):
    """Manage configuration."""
    if show:
        settings = get_settings()
        console.print("📋 Current Configuration:", style="bold blue")
        console.print(f"  App Host: {settings.app_host}")
        console.print(f"  App Port: {settings.app_port}")
        console.print(f"  Debug: {settings.debug}")
        console.print(f"  Log Level: {settings.log_level}")
        console.print("")
        console.print("🤖 LLM Configuration:", style="bold blue")
        console.print(f"  Ollama URL: {settings.ollama_base_url}")
        console.print(f"  Default Model: {settings.default_model}")
        console.print(f"  Alternate Model: {settings.alternate_model}")
        console.print(f"  Code Model: {settings.code_model}")
        console.print(f"  Embedding Model: {settings.embedding_model}")
        console.print(f"  GPU Enabled: {settings.enable_gpu}")
        console.print("")
        console.print("🔍 Search Configuration:", style="bold blue")
        console.print(f"  SearXNG URL: {settings.searxng_url}")
        console.print(f"  Web Scraping: {settings.enable_web_scraping}")
        console.print("")
        console.print("📁 Storage Configuration:", style="bold blue")
        console.print(f"  Upload Dir: {settings.upload_dir}")
        console.print(f"  Output Dir: {settings.output_dir}")
        console.print(f"  Cache Dir: {settings.cache_dir}")
        console.print("")
        console.print("🔒 Security Configuration:", style="bold blue")
        console.print(f"  Max File Size: {settings.max_file_size} bytes")
        console.print(f"  Allowed Extensions: {settings.allowed_extensions}")
        console.print(f"  Rate Limit: {settings.rate_limit_per_minute}/min")
    else:
        console.print("Use --show to display current configuration", style="bold yellow")


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
