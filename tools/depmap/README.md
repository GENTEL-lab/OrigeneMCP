# DepMap MCP Tool

Cancer cell line analysis tool that provides comprehensive cancer genomics data query services via the MCP protocol.

## Features

- CRISPR dependency analysis
- RNA-seq expression analysis
- Mutation pattern analysis
- Comprehensive multi-dimensional analysis

## Configuration

Set in `default.conf.toml`:

```toml
depmap_data_dir = "/home/zhongzhenyi/project/depmap"
```

## Startup

```bash
# Stdio mode
python -m tools.depmap.server

# HTTP mode
python -m tools.depmap.deploy
```

## Usage

Provides 4 tool functions:
- depmap_get_dependency
- depmap_get_expression
- depmap_get_mutation
- depmap_comprehensive_analysis

See the tool documentation in server.py for details.
