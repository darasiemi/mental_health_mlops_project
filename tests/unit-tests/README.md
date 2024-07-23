First, you need to select your Python interpreter which houses your dependencies. This can be done by `CMD+Shift+P` on VS Code(MacOS). Then enter the path `path-to-you-environment/bin/python`. 


To run pytest, cd to the unit-tests directory. The `--disable-warnings` to avoid warnings that clutter the terminal 
```bash
pytest model_test.py --disable-warnings
```