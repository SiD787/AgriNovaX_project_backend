# Design System Specification: Modern Pastoral Editorial

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"Modern Pastoral Editorial."** 

Agriculture is inherently tactile, seasonal, and grounded. To move beyond a generic "SaaS dashboard" feel, this design system treats data like a high-end gardening journal. We replace the rigid, clinical grids of traditional software with an editorial layout that prioritizes breathing room, sophisticated tonal depth, and a sense of "organic order." 

The system avoids the "template" look by utilizing intentional asymmetry—placing hero metrics off-center or allowing imagery to bleed across container boundaries—creating a digital experience that feels as natural and premium as the land it manages.

---

## 2. Colors & Surface Architecture
The palette is a curated selection of forest greens, rich loams, and atmospheric neutrals.

### The "No-Line" Rule
Standard 1px borders are strictly prohibited for sectioning. Structural definition must be achieved through **Tonal Shifts**. To separate a sidebar from a main content area, transition from `surface` (#f9faf6) to `surface_container_low` (#f3f4f0). This creates a sophisticated, "borderless" interface that feels expansive rather than boxed-in.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the following hierarchy to define depth:
1.  **Base Layer:** `surface` (#f9faf6) — The canvas.
2.  **Section Layer:** `surface_container_low` (#f3f4f0) — Defines broad content areas.
3.  **Component Layer:** `surface_container_lowest` (#ffffff) — Used for primary cards to create a "lifted" effect against the section layer.
4.  **Emphasis Layer:** `surface_container_high` (#e7e9e5) — For inset elements like search bars or secondary utility panels.

### The Glass & Gradient Rule
To inject "soul" into the interface:
*   **CTAs:** Use a subtle linear gradient (top-down) from `primary` (#3d6631) to `primary_container` (#557f47). This avoids the flatness of standard buttons.
*   **Overlays:** Use Glassmorphism for floating navigation or weather alerts. Apply `surface` at 70% opacity with a `16px` backdrop-blur to allow the earthy background colors to bleed through.

---

## 3. Typography
We utilize **Inter** across all scales. The goal is "High-Readability Editorial"—large headers for high-impact data and generous line-heights for instructional text.

*   **Display (lg/md/sm):** Used for "Hero Numbers" like soil moisture percentages or temperature. The large scale acts as a visual anchor.
*   **Headline (lg/md/sm):** For section titles. These should have a slightly tighter tracking (-0.02em) to feel authoritative and "set" like a magazine header.
*   **Body (lg/md):** Primary reading font. Ensure a line-height of 1.6 to maintain approachability for non-technical users.
*   **Label (md/sm):** Reserved for metadata (e.g., "Last synced 2m ago"). Use `on_surface_variant` (#42493f) to keep these secondary to the main content.

---

## 4. Elevation & Depth
Depth is communicated through light and layering, never through heavy shadows or lines.

*   **The Layering Principle:** Rather than adding a shadow to a card, place a `surface_container_lowest` card on top of a `surface_container` background. The subtle shift in hex value provides a natural, soft "lift."
*   **Ambient Shadows:** If an element must float (e.g., a "New Crop" FAB), use an extra-diffused shadow: `box-shadow: 0 12px 40px rgba(26, 28, 26, 0.06);`. The shadow color is a tinted version of `on_surface`, avoiding the "dirty" look of pure black shadows.
*   **The "Ghost Border" Fallback:** In high-density data tables where tonality isn't enough, use a "Ghost Border": 1px solid `outline_variant` at **15% opacity**.

---

## 5. Components

### Cards & Lists
*   **Styling:** No borders. Use `md` (0.75rem) or `lg` (1rem) corner radius.
*   **Separation:** Forbid the use of divider lines. Separate list items using `16px` of vertical white space or by alternating background tones between `surface` and `surface_container_low`.

### Buttons
*   **Primary:** Gradient of `primary` to `primary_container`. Text in `on_primary`. 
*   **Secondary:** Solid `secondary_fixed`. A soft, earthy brown that feels tactile.
*   **Tertiary:** No background. Use `primary` text.

### Inputs & Selection
*   **Input Fields:** Use `surface_container_high` for the field body with a 0.5rem radius. When focused, use a `2px` "Ghost Border" of `primary`.
*   **Chips:** Use for crop types (e.g., "Wheat," "Corn"). Use `secondary_container` for unselected and `primary` for selected.
*   **Checkboxes/Radio:** Must use the `primary` color for the "checked" state. Ensure the hit target is at least `48px` for ease of use in the field.

### Domain-Specific Icons (Custom Style)
Icons should be monolinear (1.5px stroke) with slightly rounded terminals to match the `md` roundedness scale.
*   **Soil:** A composition of three horizontal organic lines of varying lengths.
*   **Crops:** A stylized sprout emerging from a `primary` toned arc.
*   **Weather:** A sun partially obscured by a cloud, using `tertiary` for sun accents.

---

## 6. Do's and Don'ts

### Do
*   **Do** use white space as a structural element. If a layout feels cluttered, increase the gap before adding a line.
*   **Do** use `display-lg` for the most important number on the screen.
*   **Do** use the `secondary` brown tones to highlight "earth-based" actions like tilling or planting.

### Don't
*   **Don't** use 100% black (#000000) for text. Use `on_surface` (#1a1c1a) for a softer, premium feel.
*   **Don't** use standard "Drop Shadows." Only use the Ambient Shadow specification.
*   **Don't** use high-contrast borders. If a container needs a boundary, use a "Ghost Border" or a tonal shift.