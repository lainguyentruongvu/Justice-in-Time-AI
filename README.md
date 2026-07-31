# Justice in Time AI — Gemini Engine v2.1

A modular **Google Gemini API** engine for the Justice in Time True Crime YouTube workflow. It compiles Core, Brand, Style, Rules, Task, Data, and Workflow Markdown modules into one structured system instruction.

## 1. Install

Requires Python 3.10 or newer. On your Windows computer, open CMD in the project folder and run:

```cmd
py -m pip install -r requirements.txt
```

The project uses Google's official `google-genai` Python SDK. It no longer uses the OpenAI package.

## 2. Create a Gemini API key

1. Open Google AI Studio.
2. Create or copy a Gemini API key.
3. Open `.env` in this project.
4. Add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
MAX_OUTPUT_TOKENS=4000
TEMPERATURE=0.7
```

Do not add quotation marks around the key. Do not publish or share `.env`.

> A Gemini/Google subscription and Gemini API billing or quota are separate products. API availability and limits depend on the Google Cloud project connected to the key.

## 3. Test the connection

```cmd
py test_gemini.py
```

Expected output:

```text
Gemini connection successful
```

## 4. Run the command-line engine

```cmd
py run.py
```

Choose a task, paste input, then type `END` on a separate line.

Other examples:

```cmd
py run.py --list
py run.py jit_comment --text "Create comments for this video topic..."
py run.py jit_script --input case_notes.txt
py run.py jit_script --show-prompt
py run.py jit_titlevideo --model gemini-2.5-flash --text "Video topic..."
```

Results are automatically saved in `outputs/`. Add `--no-save` to disable saving.

## 5. Run the web chat interface

```cmd
py -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

The sidebar lets you select the task, Gemini model, language, tone, and whether to preview the compiled system prompt.

## 6. Available tasks

- Comment: `jit_comment`, `jit_reply`
- Content: `jit_hook`, `jit_script`, `jit_community`
- SEO: `jit_titlevideo`, `jit_desc`
- Analytics: `jit_ctr`, `jit_retention`, `jit_analytics`
- Workflows: `workflow_comment`, `workflow_video`, `workflow_upload`, `workflow_analytics`, `workflow_complete`

## 7. Module architecture

```text
00_CORE/       Global identity, brand, style, and rules
01_COMMENT/    Comment and reply tasks
02_CONTENT/    Hooks, scripts, and community posts
03_SEO/        Titles and descriptions
04_ANALYTICS/  CTR, retention, and performance analysis
05_DATA/       Reusable audience and example data
06_WORKFLOWS/  Multi-stage workflow instructions
engine/        Python runtime
outputs/       Generated results
```

Task dependencies are declared in `engine/registry.py`.

## 8. Common errors

### `GEMINI_API_KEY is missing`
Add the key to `.env`, save the file, then restart CMD or Streamlit.

### `google-genai is not installed`

```cmd
py -m pip install -r requirements.txt
```

### Error 429 / quota exceeded
The key's Google project has reached a request or token limit. Check usage, rate limits, billing, or wait for the quota window to reset.

### Model not found
Change `.env` to a Gemini model available to your API project, for example:

```env
GEMINI_MODEL=gemini-2.5-flash
```

## 9. Security

- Never upload `.env` to a public repository.
- If a key has been exposed, revoke it and create a new one.
- Only `.env.example` should be shared publicly.
