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
- [ ] Define CLI command structure (pixelate vs grid)
- [ ] Implement argument parsing and validation
- [ ] Map CLI options to internal config objects
- [ ] Implement output path handling and overwrite rules
- [ ] Add helpful error messages and --help text

## Pipeline
- [ ] Define transformation pipeline (load → transform → save)
- [ ] Ensure pipeline is deterministic and side-effect free
- [ ] Support RGB and RGBA images cleanly

## Testing
- [ ] Add unit tests for pixelation output dimensions
- [ ] Add unit tests for grid resizing correctness
- [ ] Add CLI argument parsing tests
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
