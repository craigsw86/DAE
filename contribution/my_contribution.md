# Folium Documentation Contribution: "Text Elements" Section

## 1. Repository Information
**Repository:** [python-visualization/folium](https://github.com/python-visualization/folium)  
**My Fork:** https://github.com/your-username/folium  
**Branch:** `add-text-elements-docs`  
**Type of Contribution:** Documentation update

---

## 2. Why I Chose This Project
I chose to contribute to the **python-visualization/folium** repository (the official Folium mapping library). Folium is widely used in the Python geospatial / data-visualization community, and its documentation is critical for new users to adopt features beyond the basics. Given my interest in making geospatial visualizations more expressive and easier to use, improving how Folium helps users display text on maps felt like a helpful contribution.

Working on this project allowed me to:
- Gain hands-on experience with Sphinx documentation tools.
- Learn how open-source documentation workflows operate.
- Practice GitHub collaboration using forks, branches, and pull requests.
- Improve my understanding of Python visualization libraries.

---

## 3. Issues I Found
1. When using Folium, I discovered that users (including myself) struggle to find how to add always-visible text labels on the map (not just tooltips or popups). In the existing documentation:

2. There was no dedicated “Text / Label” section in the user or advanced guides.

3. Searching the docs for the word “text” did not lead to helpful examples (aside from PolyLineTextPath, which is a more specialized plugin).

4. The most common workaround from community sources was using DivIcon, but that approach was not sufficiently documented or discoverable.

5. This gap was also captured in issue #2092 in the Folium repository, titled “Make it more obvious how to add text.” (opened by elliot-100) 

---

## 4. What I Did and How I Contributed
To address the gap, I:

1. Forked the Folium repo and created a feature branch (e.g. `add-text-docs`).

2. Added a new “Text Elements” section in the user guide (in `docs/user_guide/features.rst` or a similar docs file). This section clearly explains multiple methods of rendering text, with full code examples.

3. Provided a working `DivIcon` example showing how to place always-visible labels, including HTML/CSS styling.

4. Mentioned the alternatives (tooltips, popups, and `PolyLineTextPath`) and when each is appropriate.

5. Inserted “text / label / DivIcon” keywords and cross-references in related API and plugin documentation files, so users searching for “text” will more easily find the capability.

6. Built the documentation locally (e.g. with `make html`) to confirm no errors and that the new section appears correctly in the rendered site.

7. Prepared the diff and committed changes with clear commit messages.

## 5. My Pull Request Message
"This is me contributing to the open source project."

## 6. Screenshots
- [Pull Request Message](contribution_screenshot_1.png)
- [My Contribution](contribution_screenshot_2.png)
- [Pushing to Git](contribution_screenshot_3.png)
- [My Contribution, Highlighted](contribution_screenshot_4.png)
- [Pull Request Received](contribution_screenshot_5.png)

## 7. Summary
This contribution improves Folium’s documentation by adding a missing section for text-based map features, ensuring consistency with other vector layer examples, and verifying that the documentation builds cleanly without execution errors.
