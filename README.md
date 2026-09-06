# Cooking notebook

A photo-first recipe site. Add a markdown file, push, and the site rebuilds
itself. No build tools, no npm, nothing to run on your machine.

---

## Putting it online (once, about five minutes)

1. On GitHub, create a new **public** repository. Name it `recipes` — or name it
   `yourusername.github.io` if you want the site at the root of your domain.

2. Upload everything in this folder to the repo. Either drag the files into
   GitHub's web uploader, or from a terminal:

   ```sh
   git init
   git add .
   git commit -m "First cook"
   git branch -M main
   git remote add origin https://github.com/YOURNAME/recipes.git
   git push -u origin main
   ```

3. In the repo, go to **Settings → Pages**. Under *Build and deployment*, set
   Source to **Deploy from a branch**, branch **main**, folder **/ (root)**.
   Save.

4. Open `_config.yml` and set `url` and `baseurl`:

   | Repo named | `url` | `baseurl` |
   |---|---|---|
   | `yourusername.github.io` | `https://yourusername.github.io` | `""` |
   | `recipes` (or anything else) | `https://yourusername.github.io` | `"/recipes"` |

   Getting `baseurl` wrong is the one mistake that breaks images and links, so
   it's worth a second look.

5. Wait a minute or two. Your site is live at the address shown on the Pages
   settings screen.

Every push after this rebuilds the site automatically, usually within a minute.

---

## Making it yours

Everything personal lives in **`_config.yml`**: the site name, the tagline, the
one-line description that opens the home page, your name, and your Instagram
handle. Edit that file and nothing else needs to change.

Then rewrite `about.md` in your own words.

---

## Adding a recipe

Two steps.

**1. Add the photo.** Put it in `assets/images/recipes/`, named after the dish.

**2. Add the recipe.** Copy `_templates/recipe.md` into the `_recipes/` folder
and rename it — the filename becomes the web address, so
`charred-cabbage.md` lands at `/recipes/charred-cabbage/`.

The top of the file, between the `---` lines, is the structured part:

```yaml
---
title: Charred cabbage, brown butter, hazelnut
date: 2026-08-28
serves: 2
time: 40 min
image: /assets/images/recipes/charred-cabbage.jpg
tags: [vegetables, weeknight]
intro: The cut side goes almost black. That is the point of the dish.
ingredients:
  - 1 small hispi cabbage
  - 90 g unsalted butter
---
```

Below that second `---`, write the method as a numbered list. The site handles
the numbering, the hanging indents and the spacing.

That's it. Commit, and the recipe appears on the home page.

### Front matter reference

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Shown everywhere. Keep it under about eight words so the large type stays on two lines. |
| `date` | yes | `YYYY-MM-DD`. Newest recipe becomes the large image on the home page. |
| `image` | no | Path from the site root, starting with `/assets/`. Without one, the tile shows a quiet blank frame rather than breaking. |
| `serves` | no | Any text: `2`, `4–6`, `a crowd`. |
| `time` | no | Any text: `40 min`, `1 hr 20`, `overnight`. |
| `intro` | no | One sentence under the title. |
| `tags` | no | Powers the filter buttons on the Recipes page. Reuse the same words and the list stays short. |
| `ingredients` | yes | A list. Use groups if the recipe has parts — see the template. |
| `notes` | no | Substitutions, warnings, leftovers. Rendered under the method. |
| `gallery` | no | Extra photos, shown two-up at the bottom. |

---

## Looking at it before you publish

Open `_preview/index.html` in a browser. It's a static snapshot of the design
that needs nothing installed. It doesn't update on its own — run
`python3 _preview/render.py` to refresh it after adding recipes, or just push
and look at the real site.

If you'd rather have a proper live preview with Ruby installed:

```sh
bundle install
bundle exec jekyll serve
```

Folders starting with `_` that aren't `_layouts`, `_includes` or `_recipes`
(so `_preview` and `_templates`) are ignored when the real site is built. They
never appear online.

---

## How it's put together

| | |
|---|---|
| `_config.yml` | Your details. The only file with anything personal in it. |
| `_recipes/` | One markdown file per recipe. This is where you spend your time. |
| `assets/images/recipes/` | Photographs. |
| `assets/css/main.css` | The whole design, in one commented file. |
| `_layouts/`, `_includes/` | Page structure. Leave alone unless you want to change how pages are built. |
| `index.html`, `recipes.html`, `about.md` | The three pages. |

### Changing the look

Every colour and typeface is declared once at the top of
`assets/css/main.css`, under `:root`. Change `--paper` and `--ink` there and the
entire site follows, dark mode included. The design deliberately has no accent
colour — the photographs are the only colour on the page, which is what keeps
the food looking like the point of it.
