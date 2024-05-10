from app.utils.openapi import generate_spec
from app.main import create_app
import json, sys

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Swagger UI</title>
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui.css" >
  <style>
    html
    {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *,
    *:before,
    *:after
    {
      box-sizing: inherit;
    }
    body {
      margin:0;
      background: #fafafa;
    }
  </style>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-bundle.js"> </script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-standalone-preset.js"> </script>
<script>
window.onload = function() {
  var spec = %s;
  console.log(spec)
  // Build a system
  const ui = SwaggerUIBundle({
    spec: spec,
    dom_id: '#swagger-ui',
    deepLinking: true,
    // presets: [
    //   SwaggerUIBundle.presets.apis,
    //   SwaggerUIStandalonePreset
    // ],
    // plugins: [
    //   SwaggerUIBundle.plugins.DownloadUrl
    // ],
    // layout: "StandaloneLayout",
    supportedSubmitMethods: [],  // makes sure no try it out
    defaultModelsExpandDepth: -1  // get rid of the top bar
  })
  window.ui = ui
}
</script>
</body>
</html>
"""

# spec = yaml.load(sys.stdin, Loader=yaml.FullLoader)

if __name__ == "__main__":

    spec: dict = generate_spec(app=create_app())
    sys.stdout.write(TEMPLATE % json.dumps(spec))


# python create_doc_html.py > index.html (how to run)
