import importlib.util
from fasthtml.components import ft_html
from air.generator import Plugin


class FastHTMLPlugin(Plugin):
    def run(self) -> None:
        print("Running FastHTMLPlugin...")
        print(f"Source dir: {self.generator.source_dir}")
        for path in self.generator.source_dir.rglob("*.py"):
            print(f"Converting {path} to HTML...")
            relative_path = path.relative_to(self.generator.source_dir)
            output_path = self.generator.output_dir / relative_path.with_suffix(".html")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # For each route in the FastHTML app, execute the function to generate the HTML and write out a file
            spec = importlib.util.spec_from_file_location("fasthtml_app", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Access the app and router
            app = getattr(module, 'app', None)
            rt = getattr(module, 'rt', None)

            if not app or not rt:
                print("Could not find 'app' or 'rt' in the module.")
                continue

            # Get all routes
            routes = app.routes

            # Execute each route's function to get the HTML
            for route in routes:
                if route.methods and 'GET' in route.methods:
                    print(f"\nExecuting route: {route.path}")
                    func = route.endpoint
                    result = func(request=None)
                    print(f"Result: {result}")

                    # Write the result to the output file
                    route_output_path = output_path.with_name(route.path.strip('/').replace('/', '_') + '.html')
                    with open(route_output_path, "w", encoding="utf-8") as f:
                        f.write(ft_html(result))

        print("FastHTMLPlugin done.")
