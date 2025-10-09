# Best Practices Setup for AI-Augmented Engineering

Now that you've created your first Air application and seen how straightforward it can be to build with the framework, let's optimize your development environment for maximum AI collaboration. In the previous chapter, you:

- Created an Air project using `uv init`
- Set up a virtual environment with `uv venv`
- Installed Air and its dependencies with `uv add`
- Built and ran your first application with `fastapi dev`

These are all great first steps! Now, to maximize the effectiveness of AI on your Air project, you will need to set up various standard Python tools, and an AI coding agent.

!!! note "Vibe Engineering? A Note from Audrey"

    Vibe engineering[1] is a new term coined by Simon Willison and currently being explored by me, Audrey M. Roy Greenfeld. It's like vibe coding, but with a focus on maintainability, code quality, clean architecture, and ability of AI agents to work with the codebase. In a way it's potentially the opposite of vibe coding because all you care about is having a great codebase, regardless of the end product.

    Here in this book our focus is on helping you set up your Air codebase to follow AI-assisted engineering best practices from the start, a field where we're all still working out what those best practices are. 
    
    I'm still exploring whether to formally call it vibe engineering in this book, or something else. Terminology matters. Let's experiment and get this right, and update this chapter embracing this or another term soon.

[1]: https://simonwillison.net/2025/Oct/7/vibe-engineering/

## AI-First and AI-Native Design

At our indie research lab [Feldroy](https://www.feldroy.com) our core research question is, "How can we evolve the field of web development in the age of AI?" Air is our experiment in which we prioritize AI agent collaboration as a first-class citizen in the development process.

Air's foundational principle is to be deeply AI-native, with every function, class, module, and documentation page optimized for AI agents to generate and interact with code effectively. This represents our framework's core identity. 

All Air core and package code from us is optimized for AIs. Naturally, that makes it great for humans to work with as well.

## Air's Principles Apply to Your Codebase

When you build with Air, you should write code as if it were going into an official Air package or Air core. Specifically, you must also optimize your own codebase for AI collaboration. 

Follow these principles, which are extended from Air core:

- Every function should include comprehensive docstrings for AI understanding, because these help with AI context.
- Type hints should be extensive and precise for AI code completion, and used by AI to validate its code by running type checkers.
- Documentation should be written to be concise and clear for both humans and LLMs. Start with clear docstrings, then document anything that AI has trouble figuring out on its own. 
- Aggressively remove comments that are blatantly obvious. AI often adds unnecessary comments to code, and it's your responsibility to fight that from the start. Only meaningful or truly helpful comments are allowed.
- Keep code flat. Reduce abstraction and functions calling functions calling functions to a bare minimum.
- Testing should be thoughtful and comprehensive, using pytest and coverage. AI agents can run pytest to check that they didn't break things, and add to tests. Write/curate the starting tests by hand, as AI will follow your patterns.
- Code structure follows predictable patterns that AI agents can easily navigate. Break up long files meaningfully so AI agents can selectively choose portions to read into context.
- Be strict about naming. Name everything carefully and precisely. Use AI to help you with naming. Make names self-documenting. No 1-2 letter variable or function names.
- Reduce cognitive load for both humans and AIs. Be expressive yet compact. Use bulleted cheatsheet-style lists and tables. Don't take "smart" coding shortcuts like `import *` or doubly-nested list comprehensions.
- Teach a human or AI how to fish. Teach them useful commands, so they can explore and extend them. Don't have them blindly follow recipes.
- Maximize observability. Use Playwright to provide screenshots to multimodal AI agents. Log liberally. Define and use custom exceptions.

We'll now set up your project and development environment with the necessary tools to support these principles.

## Linting and Formatting: Ruff

Ruff is a fast Python linter and code formatter that helps maintain a clean and consistent codebase. Air uses Ruff for both linting and formatting, ensuring consistent code style across the project.

Install Ruff as a dev dependency with uv:

```bash
uv add --dev ruff
```

Then run all of these commands on your code to check for style and linting issues, fix any fixable issues, and format your code:

```bash
ruff check .
ruff check --fix .
ruff format .
```

Air's configuration for Ruff is defined in its `pyproject.toml` file, at https://github.com/feldroy/air/blob/main/pyproject.toml

To start, most people won't need custom Ruff configuration. If you do, add a `[tool.ruff]` section to your own project's `pyproject.toml` file. See the [Ruff documentation](https://docs.ruff.rs/) for configuration options.

After setting up Ruff and running the commands, commit these changes:

```bash
git add .
git commit -m "Add Ruff, and have it auto-fix issues and format code"
```

## Type Checkers: Ty and Pyrefly

Air recommends using `ty` and `pyrefly` instead of MyPy for type checking. `ty` and `pyrefly` are tools built specifically for Air projects that provide helpful type checking without the noise that MyPy produces on Air projects. This is because MyPy will print errors that are not helpful if you run it on the current main.py file.

Install both tools as dev dependencies with uv:

```bash
uv add --dev ty pyrefly
```

Run Ty on your project to check for type errors:

```bash
ty check
```

Run Pyrefly to analyze your project's dependencies and structure:

```bash
pyrefly check
```

Both tools provide better integration with Air's type system and are designed to be more helpful for Air projects specifically.

After setting up ty and pyrefly and running the checks, commit these changes:

```bash
git add .
git commit -m "Add ty and pyrefly for type checking"
```

## Testing: PyTest and Coverage

Testing is crucial for maintaining code quality and ensuring your application works as expected. PyTest is the preferred testing framework for Python projects, including Air. It makes writing and running tests simple and intuitive for both humans and AI coding assistants.

Install PyTest and coverage tools with uv:

```bash
uv add --dev pytest pytest-cov
```

Create test files in your project, typically with names starting with `test_` or ending with `_test.py`. Here's an example test:

```python
def test_greeting():
    """Test that the greet function returns the expected string."""
    result = greet("World")
    assert result == "Hello, World!"
```

Run your tests using PyTest:

```bash
pytest
```

To see test coverage information, run:

```bash
pytest --cov=.
```

This will show you which parts of your code are covered by tests. Aim for high test coverage to ensure your AI coding assistant can confidently modify code without breaking existing functionality.

Configure PyTest by adding settings to your `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
]
```

Having comprehensive tests not only ensures code quality but also gives AI coding assistants confidence when making changes, as they can rely on tests to catch any regressions.

## AI Coding Agent: Qwen Code

The most popular agentic AI coding assistants today are GitHub Copilot, OpenAI Codex, Claude Code, Gemini CLI, and Qwen Code. 

You will see that it's not always about which coding agent you pick. Your productivity with AI is primarily about what's in your context window.

If you already have an agent you use, stick with it. Or use Qwen Code along with us here.

Qwen Code has the most generous free tier and works great with Air. Install it per the official instructions at [https://github.com/QwenLM/qwen-code/](https://github.com/QwenLM/qwen-code/)

Once installed, try it from within your Air project directory:

```bash
qwen
```

If you are using it for the first time, it will open a browser window to authenticate. After that, you can use it in your terminal. Try asking it a question about your main.py and see what happens.

## Provide Great Agent Instructions

If your AI coding agent reads instructions from an AGENTS.md file, create one. Otherwise install Ruler (https://github.com/intellectronica/ruler) and then use it to set up your agent instructions.

Here is a sample AGENTS.md file for Air projects:

```markdown
# Agent Instructions for Air Projects

## Project Context

- This is an Air web framework project (https://github.com/feldroy/air)
- Air is a high-level layer over FastAPI that streamlines web interface and API development
- Air emphasizes developer experience with Pythonic approaches

## Code Style & Conventions

- Use Ruff for linting and formatting: `ruff check .` and `ruff format .`
- Follow the configuration in pyproject.toml
- Run `ruff check --fix .` to automatically fix most issues
- Use comprehensive type hints for all functions, parameters, and return values
- Write clear, comprehensive docstrings for all functions, classes, and modules
- Follow the AI-native design principles of Air (predictable patterns, clear naming)

## Testing

- Use PyTest for testing
- Write tests that follow the patterns established in the existing test suite
- Aim for high test coverage using `pytest --cov=.` 
- Create test files with names starting with `test_` or ending with `_test.py`
- Run `pytest` regularly to ensure no regressions

## Type Checking

- Use MyPy for type checking: `mypy .`
- Install typing extensions as needed: `uv add --dev typing-extensions`
- Ensure all new code passes MyPy checks before committing

## Project Structure

- Air projects follow predictable patterns for routing, templates, and components
- Break up large files into meaningful modules to help with AI context limitations
- Use Air's tag system and layout components as appropriate
- Follow common Python web development patterns while leveraging Air's features

## Development Workflow

- Always run Ruff, MyPy, and PyTest before committing changes
- Use `uv` as the package manager: `uv add`, `uv add --dev`, etc.
- When adding new dependencies, use `uv add` for runtime and `uv add --dev` for development
- Check your work with the tools before asking humans to review
```

## Tell the Agent to Check Your Code

One of the most powerful aspects of using an AI coding assistant is its ability to review and improve your existing code. After setting up your development environment with proper linting, type checking, and testing, you can ask your AI coding assistant to review your code quality.

When using Qwen Code or another AI assistant, you can prompt it to:

- Review your code for adherence to best practices
- Identify potential bugs or issues
- Suggest improvements based on the tools you've set up (Ruff, MyPy, PyTest)
- Help fix any issues found by these tools

For example, you can ask your AI assistant:

```
Review my project for code quality issues and ensure it follows the setup described in the documentation.
```

Or more specifically:

```
Help me fix any issues found by Ruff, MyPy, and Pytest in my project.
```

This ensures that your AI coding assistant is aligned with your project's standards and can help maintain code quality as you develop.

## Including the Air Codebase for AI Context

To further enhance your AI coding assistant's ability to understand and work with Air's functionality, you can add the Air repository as a git submodule to your project. This allows AI agents to read the core Air codebase files directly, giving them deeper insight into how the framework works internally.

From within your project directory, add the Air repository as a submodule:

```bash
git submodule add https://github.com/feldroy/air.git
```

This will create an `air` directory in your project that contains the Air source code. AI coding assistants can then reference these core files when generating code or answering questions about Air's implementation details.

After adding the submodule, commit the change:

```bash
git add .gitmodules air
git commit -m "Add Air core codebase as git submodule for AI context"
```

## Summary

Setting up your AI-enhanced development environment with proper tooling (Ruff, MyPy, PyTest) creates a foundation where both humans and AI coding assistants can work more effectively together. The tools provide clear, consistent feedback on code quality, type safety, and test coverage, enabling better collaboration between developers and AI systems.

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Set up AI-enhanced development tools: Ruff, MyPy, PyTest, AGENTS.md, and Air core submodule"
```

With these tools in place, you're now ready to build more sophisticated applications with Air, leveraging both the framework's capabilities and AI assistance for enhanced productivity.
