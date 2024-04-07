from confluence_api import Confluence

# Replace with your Confluence server URL, username, and password
confluence_url = "https://your-confluence-server.atlassian.net"
username = "your_username"
password = "your_password"

# Create Confluence API client
confluence = Confluence(
    url=confluence_url,
    username=username,
    password=password
)
def get_confluence_data(space_key):
  """
  Extracts page content from a Confluence space

  Args:
      space_key: The key of the Confluence space

  Returns:
      A list of dictionaries containing page titles and content
  """
  pages = confluence.get_all_pages(space_key)
  data = []
  for page in pages:
    page_data = {
      "title": page.title,
      "content": confluence.get_page_by_id(page.id).content
    }
    data.append(page_data)
  return data

def preprocess_data(data):
  """
  Preprocess extracted data (optional)

  Args:
      data: A list of dictionaries containing page titles and content

  Returns:
      A list of preprocessed data (e.g., cleaned text)
  """
  # Implement your desired data cleaning/preprocessing logic here
  # (e.g., remove HTML tags, convert to plain text, etc.)
  preprocessed_data = []
  for item in data:
    # Your preprocessing logic goes here
    preprocessed_data.append(item)
  return preprocessed_data
