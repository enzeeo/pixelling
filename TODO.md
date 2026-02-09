# pixkit TODO

## Project setup
- [x] Choose final project name
- [x] Initialize Git repository
- [x] Create pyproject.toml with dependencies and CLI entry point
- [ ] Add .gitignore and LICENSE

## Core image operations
- [x] Implement block-size pixelation operation
- [x] Implement grid-based resize operation (fixed width/height)
- [x] Implement optional color quantization
- [x] Centralize resize helpers and resampling choices

## CLI
- [x] Define CLI command structure (pixelate vs grid)
- [x] Implement argument parsing and validation
- [x] Map CLI options to internal config objects
- [x] Implement output path handling and overwrite rules
- [x] Add helpful error messages and --help text

## Pipeline
- [x] Define transformation pipeline (load → transform → save)
- [ ] Ensure pipeline is deterministic and side-effect free
- [x] Support RGB and RGBA images cleanly

## Testing
- [x] Add unit tests for pixelation output dimensions
- [x] Add unit tests for grid resizing correctness
- [x] Add CLI argument parsing tests
- [ ] Add small test images to test/assets

## Documentation
- [ ] Write README with usage examples
- [ ] Add before/after example images
- [ ] Document pixelation vs grid modes
- [ ] Document common recipes and parameter choices

## Polish / future extensions
- [ ] Batch directory processing
- [ ] Animated GIF support
- [ ] Video frame pixelation
- [ ] Preset styles (e.g. low-res, chunky, clean)
