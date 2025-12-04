## Storage Configuration

The GIS MCP Server uses a configurable storage directory for file operations (reading, writing, and downloading data). By default, files are stored in `~/.gis_mcp/data/`.

### Specifying a Custom Storage Folder

You can specify a custom storage folder using either:

1. **Command-line argument:**

   ```bash
   gis-mcp --storage-path /path/to/your/storage
   ```

2. **Environment variable:**

   ```bash
   export GIS_MCP_STORAGE_PATH=/path/to/your/storage
   gis-mcp
   ```

On Windows PowerShell:

```powershell
$env:GIS_MCP_STORAGE_PATH="C:\path\to\your\storage"
gis-mcp
```

### Default Storage Location

If no storage path is specified, the server uses the default location:

- **Default path:** `~/.gis_mcp/data/`
  - Linux/Mac: `/home/username/.gis_mcp/data/`
  - Windows: `C:\Users\username\.gis_mcp\data\`

The storage directory is automatically created if it doesn't exist.

### How Storage Works

- **File writes:** When you save files using tools like `write_file_gpd`, `write_raster`, or `save_results`, relative paths are resolved relative to the storage directory. Absolute paths are used as-is.
- **Data downloads:** Downloaded data (satellite imagery, climate data, movement networks, etc.) is saved to subdirectories within the storage folder:
  - `movement_data/` - Street networks
  - `land_products/` - Land cover data
  - `satellite_imagery/` - Satellite imagery
  - `ecology_data/` - Species occurrence data
  - `climate_data/` - Climate datasets
  - `administrative_boundaries/` - Administrative boundaries
  - `outputs/` - General output files

### Example Configuration for MCP Clients

For Claude Desktop or Cursor IDE, you can specify the storage path in your configuration.

**Claude Desktop / Cursor (JSON config):**

```json
{
  "mcpServers": {
    "gis-mcp": {
      "command": "/home/YourUsername/.venv/bin/gis-mcp",
      "args": ["--storage-path", "/custom/path/to/storage"]
    }
  }
}
```

On Windows, adjust the command path accordingly, for example:

```json
{
  "mcpServers": {
    "gis-mcp": {
      "command": "C:\\\\Users\\\\YourUsername\\\\.venv\\\\Scripts\\\\gis-mcp",
      "args": ["--storage-path", "C:\\\\custom\\\\path\\\\to\\\\storage"]
    }
  }
}
```

### Environment Variable Configuration

Instead of passing `--storage-path`, you can configure the environment variable in your shell profile:

```bash
export GIS_MCP_STORAGE_PATH=/custom/path/to/storage
```

Or in PowerShell:

```powershell
$env:GIS_MCP_STORAGE_PATH="C:\custom\path\to\storage"
```

This ensures all future `gis-mcp` runs use the specified storage directory by default.
