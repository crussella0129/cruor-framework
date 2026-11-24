# Sprint 1 Test Plan

Rust tests are named as plain identifiers; Python tests begin `test_`;
checks made by a person begin `review_`. Each task's tests are written with
the task and land in its commit. Tests that open a page do so in one
engine, Chromium, as the specimen's test does; what other engines draw is
judged by eye and is not claimed here.

Tests that run over the furniture read one list, `tests/parts.py`, which
says of each part its class, the page that holds it, which of its text is
measured and at which bound, whether it is filled with the blood, what of it
takes the keyboard, and its states. A part is tested when it is in that
list; the list is whole when T-208 is done.

A ground is read from a picture, as it is drawn, and colours are read with
stillness asked for. A pair of colours that no single rule sets (lettering
inherited into a container, text on a tinted row) is therefore held by the
tests over the list, which measure what is drawn; the static check of
T-203 sees only a rule that sets both.

Two things a browser cannot measure are held by the theme file's entries
alone (T-203): letters with a gradient clipped to them (carved headings,
code chips), and a visited link. The open list of a `<select>` is the
system's own and is not measured. What engines other than Chromium draw,
and whether they open a dialog from a button alone, is not tested in this
sprint; backlog task T-105 carries it.

## Intent Traceability
| Intent | Acceptance criterion | Build task / EARS clause | Verification |
|--------|----------------------|--------------------------|--------------|
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 5: its own terms | T-216 / WHEN a push is about to be made THEN an entry SHALL first be added, and no push made if anything is found | `review_own_terms_before_each_push` |
| [INT-0002](../../../intents/INT-0002-cruor-web-fonts.md); [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | INT-0002 all; INT-0001 1 | T-215 / WHEN the default branch is listed THEN it SHALL hold the fonts, their licence, stylesheet and manifest, the Book and the README; INT-0002 moved to `realized`, INT-0001 1 recorded | `review_default_branch_holds_the_fonts` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 1: one TOML file states the look by role | T-201 / WHEN `look --check` reads the theme file THEN it SHALL find every key the clause names | `theme_as_written_is_complete` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 1 | T-201 / WHEN a key is lacking, or one is there that the form has not, THEN non-zero, naming the key | `theme_refuses_a_missing_key`, `theme_refuses_an_unknown_key` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 1 | T-201 / WHEN a colour is malformed THEN non-zero, naming the key | `theme_refuses_a_bad_colour` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 1: a heading's font is a role or a family the kit holds | T-201 / WHEN a font role names a family the kit does not list, or a heading's font or `seal-font` is neither a role nor such a family, THEN non-zero, naming the key; WHEN a heading's font is a family the kit holds THEN it SHALL be taken | `theme_refuses_a_family_the_kit_does_not_hold`, `theme_refuses_a_heading_font_that_is_neither`, `theme_refuses_a_seal_font_that_is_neither`, `theme_accepts_a_heading_font_by_family` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 1: the form is written up | T-201 / WHEN `look/THEME.md` is read THEN it SHALL name every table and key | `test_theme_form_names_every_key` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 2: tokens made by one command | T-202 / WHEN `look` is run THEN one rule on the class, one `--cruor-` property for every role, measure and heading setting, each with the theme's value, and nothing else | `tokens_hold_every_role`, `tokens_are_one_rule_on_the_class` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 2 | T-202 / WHEN `look` is run twice THEN byte-identical | `tokens_are_the_same_twice` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 2: a check fails if the two disagree | T-202 / WHEN `look --check` is run on a stale or absent file THEN non-zero, naming it; WHEN they agree THEN zero | `look_check_fails_on_stale_tokens`, `look_check_fails_on_absent_tokens`, `look_check_passes_on_repository` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 2 | T-202 / WHEN `check` is run THEN it SHALL fail if `look --check` would | `check_runs_the_look` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 3: each bound, on the grounds that criterion names | T-203 / WHEN the theme file is read THEN its entries SHALL hold each pair the clause names, at its ratio | `contrast_names_every_bound_of_the_look` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 3 and 4: the stone at its brightest, and it never lowers the ratios | T-203 / WHEN `look --check` is run on the theme as written THEN every entry SHALL hold, the sheen laid first and the candle over it, without rounding | `contrast_holds_for_the_look`, `contrast_lays_the_sheen_then_the_candle`, `contrast_does_not_round` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 3: the bounds are tested from the theme file | T-203 / WHEN a text colour is dimmed until an entry fails THEN non-zero, naming role, ground and ratio | `contrast_fails_naming_the_pair` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 3 | T-203 / WHEN `look` is run on a theme whose contrast fails THEN non-zero, nothing written | `look_refuses_a_theme_that_fails_contrast` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 3: every ground a role is set on | T-203 / WHEN a rule sets a text colour and a ground by tokens THEN an entry SHALL cover the pair | `test_every_text_on_ground_pair_is_promised` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 3 | T-203 / WHEN an entry names a role or ground the theme has not THEN non-zero, naming it | `contrast_refuses_an_unknown_role` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md); [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | INT-0006 4; INT-0003 3 | T-211 / WHEN the contrast of two colours is asked THEN WCAG 2's ratio | `test_contrast_helper_knows_the_ratio` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 4 | T-211 / WHEN a colour has an alpha THEN it SHALL be laid over the ground given | `test_contrast_helper_lays_alpha_over_ground` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 4 | T-211 / WHEN the ground behind lettering is asked THEN it SHALL be read from a picture with the lettering made clear, the least favourable pixel in its box | `test_ground_is_read_from_a_picture`, `test_ground_read_sees_a_gradient`, `test_ground_read_sees_a_pseudo_elements_fill`, `test_ground_read_sees_a_tint_over_what_is_beneath` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 3: the stone's brightest sheen included | T-211 / WHEN the lettering lies straight on the page under the look THEN it SHALL be held against the theme file's `stone` as well, at the value the clause gives | `test_lettering_on_the_page_is_held_against_the_stone` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 4 | T-211 / WHEN the lettering's own colour is clear THEN the helper SHALL refuse and say why | `test_helper_refuses_clear_letters` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 4: in every state | T-211 / WHEN colours are read THEN the page SHALL have been opened with stillness asked for | `test_helper_reads_with_stillness_asked` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 4: no script needed | T-211 / WHEN a page is opened with script off THEN a script in it SHALL not have run | `test_browser_opens_a_page_with_script_off` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md); [INT-0006](../../../intents/INT-0006-the-furniture.md) | INT-0003 2 and 4; INT-0006 3 | T-204 / WHEN a stylesheet of `look/` is read THEN every rule nested beneath the class, keyframes named `cruor-`, no `@import`, no `url()` but a `data:` one | `test_every_rule_sits_beneath_the_class`, `test_keyframes_are_named_for_cruor`, `test_stylesheets_fetch_nothing` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 6: what shows the look takes its colours from the theme file | T-204 / WHEN a stylesheet names a colour outside a `data:` address THEN by a token | `test_stylesheets_name_colours_by_token` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 1 and 4: the stone is shown, behind the content, with no image file | T-204 / WHEN a page that sets the class is opened THEN `<body>` SHALL have a fixed pseudo-element with a `data:` image, beneath the content, ignoring the pointer, at the token's opacity; the candle from its tokens; the ground SHALL be `page` | `test_stone_lies_beneath_the_page`, `test_candle_takes_its_tokens` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 4: it never lowers the ratios | T-204 / WHEN the bare stone is pictured at 1280 by 800 with stillness asked THEN every entry on `stone` SHALL hold against its brightest pixel, with no allowance | `test_every_bound_holds_on_the_stone_as_drawn` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 4 | T-204 / WHEN the candle's rules are read THEN no step of its flicker SHALL be stronger than the candle when still | `test_candle_is_never_stronger_than_when_still` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 1: plain HTML is dressed | T-205 / WHEN a page of plain HTML that sets the class is opened THEN paragraphs, headings, tables, code and links SHALL be set as the theme file says | `test_plain_html_is_dressed` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 1: the carved headings and the ornaments | T-205 / WHEN that page is opened THEN headings carry a clipped gradient, the seal is `seal-size` times the text, an `<hr>` draws the sigil, a quotation its channel, a list item its mark | `test_ornaments_are_drawn` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 2: a page that does not set the class is untouched | T-205 / WHEN opened without the class THEN computed styles SHALL be those of a page with no stylesheet | `test_page_without_the_class_is_untouched` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 5: motion stops when asked | T-205 / WHEN stillness is not asked THEN at least one animation runs; WHEN it is THEN none, and no element has a transition of any length | `test_look_moves_unless_asked_to_be_still`, `test_nothing_is_in_passage_when_stillness_is_asked` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 5: print is black on white with no ornament | T-205 / WHEN rendered for print THEN white ground, black text, no stone, candle, seal's shadow or sigil | `test_look_prints_plain` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 4: changing a heading level changes that heading | T-205 / WHEN a level's size, font, weight, slant or underline is changed in a copy and `look` run THEN that heading SHALL show it and the others not, for each of the five | `test_theme_changes_a_heading` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1 | T-206 / WHEN `tests/parts.py` is read THEN it SHALL give each built part's class, page, measured text and bound, whether the blood fills it, what takes the keyboard, and its states, as the plan's table gives them | `test_parts_list_is_whole` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1: each part is a rule | T-206, T-207, T-208 / WHEN `furniture.css` is read THEN a rule for the class of every part in the list, and for no other `cruor-` class | `test_furniture_has_every_part_and_no_other` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 4: text meets the bounds in every state | T-206, T-207, T-208 / WHEN a part is in any of its states THEN each text the list names for it SHALL stand at the bound the list gives, or 3 when unable | `test_every_lettered_part_meets_contrast` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1: no script | T-206 / WHEN a tick box or radio button is ticked or picked, script off, THEN what is drawn SHALL differ | `test_tick_and_radio_show_their_state` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 3: the edge a part filled with blood carries | T-206 / WHEN a part the list says is filled with the blood is shown THEN the edge of its fill SHALL stand at 3 against the ground beside it | `test_blood_carries_an_edge` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 5: reached by the keyboard, which is shown | T-206, T-207, T-208 / WHEN Tab is pressed through a page THEN every part that takes the keyboard SHALL take it and show a mark | `test_keyboard_reaches_and_marks_every_part_that_takes_it` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 5: worked by the keyboard | T-206 / WHEN Space or an arrow is pressed on a tick box, radio button, slider or choice, script off, THEN each SHALL change | `test_controls_are_worked_by_their_keys` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1, 4 and 5, of the containers | T-207 / WHEN the task is done THEN the list SHALL hold the six containers, and the list's tests hold for them | `test_parts_list_is_whole`, and the three tests over the list above |
| [INT-0006](../../../intents/INT-0006-the-furniture.md); [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | INT-0006 4; INT-0003 3 | T-207 / WHEN a paragraph is set in a plate, panel, notice of each kind, open fold or shown rise THEN an inscription of 24 pixels or more at 3.3; WHEN the void has a current row THEN its lettering 4.5 against the row | `test_paragraph_in_every_container_is_an_inscription`, `test_voids_current_row_meets_contrast` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md); [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | INT-0006 4; INT-0003 3 | T-207 / WHEN an `h1`, `h2` or `h3` is set in a container THEN it SHALL not be carved, and SHALL stand at 3.3 against the container's ground | `test_heading_in_a_container_is_not_carved` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1 and 5 | T-207 / WHEN a fold's summary is clicked or given Enter, script off, THEN open; folds sharing a name close one another | `test_fold_opens_without_script`, `test_folds_sharing_a_name_open_one_at_a_time` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1 and 5 | T-207 / WHEN a rise's button is clicked, script off, THEN shown; WHEN Escape THEN hidden | `test_rise_opens_and_closes_without_script` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md); [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | INT-0006 1 and 5; INT-0001 4 | T-207 / WHEN a button's `commandfor` names a dialog with `show-modal`, script off, THEN modal, the page behind not taking the keyboard, Escape closing it | `test_dialog_opens_modal_without_script` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1, 3, 4 and 5, of the last parts | T-208 / WHEN the task is done THEN the list SHALL hold every part of the plan's table, and the list's tests hold for all | `test_parts_list_is_whole`, and the three tests over the list above |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 1 and 5 | T-208 / WHEN a masthead is shown THEN the briar from a `data:` address; the current link and place marked by `aria-current` and by more than colour | `test_masthead_carries_the_briar`, `test_current_place_is_marked_beyond_colour` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 6: motion stops when asked | T-208 / WHEN the page of every part is opened and stillness not asked THEN an animation runs; WHEN asked THEN none, and no part has a transition of any length | `test_furniture_moves_unless_asked_to_be_still`, `test_no_part_is_in_passage_when_stillness_is_asked` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md) | 6: print is plain | T-208 / WHEN rendered for print THEN white or no ground, black text, no briar, sigil or loader | `test_furniture_prints_plain` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 1, 2 and 4 | T-209 / WHEN the showroom is opened over HTTP THEN every face SHALL load, no request fail, none go elsewhere | `test_showroom_loads_from_the_kit_alone` |
| [INT-0006](../../../intents/INT-0006-the-furniture.md); [INT-0007](../../../intents/INT-0007-the-showroom.md) | INT-0006 2; INT-0007 boundary: adds no rules but its own layout | T-209 / WHEN the page is read THEN every part in every state it has at rest; `showroom.css` holds no rule on a `cruor-` class and no pseudo-class of state | `test_showroom_shows_every_part_in_every_resting_state`, `test_showroom_imitates_no_state` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 3: beside each part the HTML that makes it | T-209 / WHEN a part is shown THEN its HTML beside it, which alone draws a part of the same size and colours | `test_showroom_gives_each_parts_html`, `test_a_parts_html_draws_the_part` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 2 | T-209 / WHEN the stylesheets are listed THEN the framework's four and `showroom.css`, which names no colour but by a token | `test_showroom_links_only_the_kit`, `test_showroom_stylesheet_adds_no_colour` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md); [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | INT-0007 boundary; INT-0001 4 | T-209 / WHEN opened with script off THEN every part SHALL still be shown | `test_showroom_stands_without_script` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | Consequences: the code family is chosen from a side by side | T-209 / WHEN the page is read THEN one line of code in each fixed-pitch family, side by side, each named | `test_showroom_sets_the_fixed_pitch_families_side_by_side` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md); [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | INT-0007 6; INT-0003 6 | T-209 / WHEN the showroom first stands THEN the owner SHALL be shown it, and the later tasks not begin until the owner has answered each of the four things asked | `review_owner_sees_the_showroom` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md); [INT-0006](../../../intents/INT-0006-the-furniture.md) | INT-0001 4; INT-0006 boundary | T-210 / WHEN tracked files are listed THEN no `.js` or `.mjs` outside `showroom/` and `examples/`, and no script element, handler attribute or `javascript:` address in HTML or SVG outside `showroom/` | `test_kit_holds_no_script` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 7: a visitor can play | T-210 / WHEN the plaything is pressed and held THEN blood SHALL fall and come to rest at the foot | `test_plaything_pours_and_pools` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 7: a part's HTML taken with one press | T-210 / WHEN the button beside a part is pressed THEN its HTML SHALL be on the clipboard | `test_copy_gives_the_parts_html` |
| [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md) | 5: motion stops when asked | T-210 / WHEN opened with reduced motion THEN the plaything SHALL move only while pressed | `test_plaything_is_still_when_asked` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md); [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md); [INT-0007](../../../intents/INT-0007-the-showroom.md) | INT-0005 1; INT-0004 5; INT-0007 boundary: no part of a release | T-212 / WHEN `bundle` is run THEN exactly a release's files and the look's four, nothing of `showroom/`, each in the manifest | `bundle_holds_exactly_a_release_with_the_look`, `bundle_manifest_lists_the_look` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 2: the same bytes every time | T-212 / WHEN `bundle` is run twice THEN byte-identical | `bundle_is_byte_identical_twice` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1 | T-212 / WHEN the tokens are stale THEN `bundle` SHALL exit non-zero and write nothing | `bundle_refuses_when_tokens_are_stale` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md); [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | INT-0005 3; INT-0001 2 | T-212 / WHEN a page in the bundle's folder links the four stylesheets by bare name and sets the class THEN every face loads and the ground is the look's | `test_release_look_works_flat` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 4: a build that fetches ends with the repository's files | T-212 / WHEN the example fetches a bundle THEN the look's four files SHALL be byte-identical to the repository's | `test_fetch_release_matches_repository` |
| [INT-0005](../../../intents/INT-0005-versioned-releases.md) | 1: a version | T-212 / WHEN the crate's manifest is read THEN `0.2.0`; the release's notes tell of the look | `test_crate_version_is_second_release`, `test_release_notes_tell_of_the_look` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 1, as settled: served by GitHub Pages | T-213 / WHEN `tools/build-site.sh` is run THEN the folder holds the showroom with the fonts and the look, and the showroom loads from it | `test_site_is_built_whole`, `test_showroom_loads_from_the_site` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 1 | T-213 / WHEN the workflow is read THEN push to `main` and by hand, guards first, publishes the script's folder, exactly three permissions, only when `SHOWROOM` is `published` | `test_pages_workflow_publishes_the_site`, `test_only_release_and_pages_may_write` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md); [INT-0006](../../../intents/INT-0006-the-furniture.md); [INT-0005](../../../intents/INT-0005-versioned-releases.md) | INT-0001 1, 2 and 4; INT-0006 7; INT-0005 6 | T-214 / WHEN the front page's words are read THEN each thing the clause names | `test_readme_says_what_the_kit_is`, `test_readme_shows_taking_the_look_on`, `test_readme_names_every_part`, `test_readme_shows_a_parts_html`, `test_readme_names_existing_paths_and_commands`, `test_readme_says_what_a_release_holds`, `test_readme_points_to_the_showroom` |
| [INT-0001](../../../intents/INT-0001-the-cruor-framework.md) | 1 | T-214 / WHEN `draw_readme.py --check` is run THEN it SHALL pass | `test_readme_pictures_are_current` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 5: a door, a picture that is a link | T-217 / WHEN `README.md` is read THEN two pictures, the door a link to the showroom with an `alt` that says so | `test_readme_is_two_pictures` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 5: a drawing | T-217 / WHEN `door.svg` is read THEN it SHALL stand alone | `test_readme_pictures_stand_alone` |
| [INT-0007](../../../intents/INT-0007-the-showroom.md) | 5 | T-217 / WHEN the check is run after the door or the words are changed by hand THEN it SHALL fail and name which | `test_readme_pictures_check_fails_on_a_changed_door`, `test_readme_pictures_check_fails_on_changed_words` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 6: what shows the look takes its colours and families from the theme file | T-218 / WHEN the script is read THEN the only colours written out SHALL be the briar's, and its four families read from the theme file's font roles | `test_front_page_writes_out_only_the_briars_colours`, `test_front_page_takes_its_families_from_the_theme` |
| [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md) | 6 | T-218 / WHEN a role is changed in a copy of the theme file and the script run THEN the picture SHALL hold the new colour and not the old | `test_front_page_takes_a_colour_from_the_theme` |

## Unit Tests

### T-201 unit tests
- **Intent:** [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- `theme_as_written_is_complete`: `look --check` on the repository → zero; the test itself lists the keys the build plan names and finds each in the file, so the list is the plan's and not the code's.
- `theme_refuses_a_missing_key`: a copy with `colour.inscription` removed → non-zero, the key named.
- `theme_refuses_an_unknown_key`: a copy with `colour.ink` added → non-zero, the key named.
- `theme_refuses_a_bad_colour`: a copy with `#12` for a colour → non-zero, the key named.
- `theme_refuses_a_family_the_kit_does_not_hold`: `font.text` set to a family not in `fonts/families.toml` → non-zero, the key named.
- `theme_refuses_a_heading_font_that_is_neither`: `heading.h2.font = "captions"` → non-zero, the key named.
- `theme_refuses_a_seal_font_that_is_neither`: `measure.seal-font = "captions"` → non-zero, the key named.
- `theme_accepts_a_heading_font_by_family`: `heading.h2.font` set to the name of a family in `fonts/families.toml` → zero, and the tokens made from it give `h2` that family.
- `test_theme_form_names_every_key`: every table and key of the theme file is found in `look/THEME.md`.
- Stubs: copies of `look/` and `fonts/families.toml` in a temporary folder, made by `tests/common/mod.rs`.

### T-202 unit tests
- **Intent:** [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- `tokens_hold_every_role`: the tokens made from the theme file → one `--cruor-` property for every colour role, role of the void, key of the stone, font role, measure and heading setting, each with the theme's value.
- `tokens_are_one_rule_on_the_class`: the file → one rule, its selector the look's class, no declaration that is not a custom property.
- `tokens_are_the_same_twice`: two runs → the same bytes.
- `look_check_fails_on_stale_tokens`: one byte changed → non-zero, the file named.
- `look_check_fails_on_absent_tokens`: the file removed → non-zero, the file named.
- `look_check_passes_on_repository`: the repository as it is → zero.
- `check_runs_the_look`: a stale tokens file → `check` fails.

### T-203 unit tests
- **Intent:** [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- `contrast_names_every_bound_of_the_look`: the test lists every pair the build plan names, with its ratio, and finds each covered by an entry at that ratio or higher.
- `contrast_holds_for_the_look`: every entry of the theme as written → meets its ratio.
- `contrast_lays_the_sheen_then_the_candle`: the `stone` ground worked by hand in the test, sheen first and candle over it → the tool's value to four places; the inscription on it → 3.31 to two places.
- `contrast_does_not_round`: an entry whose bound is one part in a thousand above the ratio found → fails.
- `contrast_fails_naming_the_pair`: the inscription dimmed → non-zero; the text role, the ground and the ratio to two places are in what is said.
- `look_refuses_a_theme_that_fails_contrast`: the same copy → `look` writes nothing.
- `contrast_refuses_an_unknown_role`: an entry naming the text role `inscripton`, and one naming the ground `stones` → each non-zero, the name given.
- `test_every_text_on_ground_pair_is_promised`: each rule of the look's stylesheets that sets `color` and a ground by tokens → the pair is in an entry. Run over each stylesheet that exists. A rule that set lettering on the blood would fail here, since no entry covers that pair.

### T-211 unit tests
- **Intent:** [INT-0006](../../../intents/INT-0006-the-furniture.md), [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md)
- `test_contrast_helper_knows_the_ratio`: black on white → 21; `#777777` on white → 4.48.
- `test_contrast_helper_lays_alpha_over_ground`: half-clear white on black → the ratio of mid grey on black.
- `test_ground_is_read_from_a_picture`: lettering on a flat ground → that ground, though the lettering has a glow of its own, which is taken off with its colour; and for a field and a choice, the pixels of the content box.
- `test_ground_read_sees_a_gradient`: lettering on a ground that runs from dark to light → the end least favourable to the lettering.
- `test_ground_read_sees_a_pseudo_elements_fill`: a ground laid by `::before` → that fill, not the element's own clear ground.
- `test_ground_read_sees_a_tint_over_what_is_beneath`: a half-clear ground over another → the colour the two make.
- `test_lettering_on_the_page_is_held_against_the_stone`: lettering straight on `<body>` under the look → measured against the theme file's `stone` as well as what is drawn; the helper's `stone` is red 31.3, green 18.8, blue 19.4, and the inscription on it 3.31, the same values the tool's test pins.
- `test_helper_refuses_clear_letters`: lettering whose colour is clear → an error that says why.
- `test_helper_reads_with_stillness_asked`: a page with an animation that never ends → opened by the helper, nothing is running when a colour is read.
- `test_browser_opens_a_page_with_script_off`: a page whose script would write a mark → no mark.
- Stubs: pages the tests write into a temporary folder; none is tracked.

### T-204 unit tests
- **Intent:** [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0006](../../../intents/INT-0006-the-furniture.md)
- `test_every_rule_sits_beneath_the_class`: each stylesheet of `look/` but the tokens, read as text → every rule nested beneath the class; rules inside `@media` and `@supports` read by their own selectors.
- `test_keyframes_are_named_for_cruor`: every `@keyframes` → a name beginning `cruor-`.
- `test_stylesheets_fetch_nothing`: no `@import`, no `url()` but a `data:` one.
- `test_stylesheets_name_colours_by_token`: no colour written out, outside a `data:` address.

### T-206, T-207 and T-208 unit tests
- **Intent:** [INT-0006](../../../intents/INT-0006-the-furniture.md)
- `test_parts_list_is_whole`: `tests/parts.py` → every part built so far, each with its class, page, measured text and bound, whether the blood fills it, what takes the keyboard, and its states; when T-208 is done, every part of the build plan's table. If the owner has a part cut, this test's count changes in the same commit as the list.
- `test_furniture_has_every_part_and_no_other`: `furniture.css` → a rule for each class in the list, and no other class beginning `cruor-`.

### T-210 unit tests
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md)
- `test_kit_holds_no_script`: `git ls-files` → no `.js` or `.mjs` outside `showroom/` and `examples/`; every tracked `.html` and `.svg` outside `showroom/` → no `<script`, no attribute beginning `on`, no `javascript:`.

### T-212 unit tests
- **Intent:** [INT-0005](../../../intents/INT-0005-versioned-releases.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- `bundle_holds_exactly_a_release_with_the_look`: the bundle's listing → the names of a release of 0.1.0 and the look's four, and no other; each of the four byte-identical to the repository's.
- `bundle_manifest_lists_the_look`: `manifest.json` → each of the four with its size and SHA-256.
- `bundle_is_byte_identical_twice`: two runs → the same bytes (Sprint 0's test, which now covers the look's files).
- `bundle_refuses_when_tokens_are_stale`: a stale tokens file → non-zero, nothing written.
- `test_crate_version_is_second_release`: `Cargo.toml` → `0.2.0` (Sprint 0's test of the first release, changed).
- `test_release_notes_tell_of_the_look`: the release workflow's notes → name the look.

### T-213 unit tests
- **Intent:** [INT-0007](../../../intents/INT-0007-the-showroom.md)
- `test_pages_workflow_publishes_the_site`: the workflow read as data → its triggers, the order of its steps, its three permissions and no other, and the condition on `SHOWROOM`.
- `test_only_release_and_pages_may_write`: every workflow → none but the release's and this one asks to write (Sprint 0's test, amended).

### T-214, T-217 and T-218 unit tests
- **Intent:** [INT-0001](../../../intents/INT-0001-the-cruor-framework.md), [INT-0006](../../../intents/INT-0006-the-furniture.md), [INT-0007](../../../intents/INT-0007-the-showroom.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- `test_readme_says_what_the_kit_is`: the words say the look is in the kit (Sprint 0's test, changed with the words).
- `test_readme_shows_taking_the_look_on`: one block of HTML links the four stylesheets and sets the class.
- `test_readme_names_every_part`: each part of `tests/parts.py` is named.
- `test_readme_shows_a_parts_html`: one block holds a part's class.
- `test_readme_names_existing_paths_and_commands`: `look/` and `showroom/` are named and exist; the commands shown are the tool's, `look` among them (Sprint 0's test, extended).
- `test_readme_says_what_a_release_holds`: the four files of the look are named among a release's.
- `test_readme_points_to_the_showroom`: the showroom's address is given.
- `test_readme_pictures_are_current`: the drawing script's check passes.
- `test_readme_is_two_pictures`: `README.md` → the page, a link to its words, and the door, a link to the showroom's address, each with an `alt`.
- `test_readme_pictures_stand_alone`: both pictures → no text that needs a font, no stylesheet, no script, no address but within itself (Sprint 0's test, now over both).
- `test_readme_pictures_check_fails_on_a_changed_door`, `test_readme_pictures_check_fails_on_changed_words`: each → non-zero, the file named.
- `test_front_page_writes_out_only_the_briars_colours`: every colour written out in `tools/draw_readme.py` → one of the briar's.
- `test_front_page_takes_its_families_from_the_theme`: the script's four families → those of the theme file's font roles, and no family's name is written out in the script.
- `test_front_page_takes_a_colour_from_the_theme`: a copy of the repository with `colour.inscription` changed → the picture drawn from it holds the new colour and not the old.

## Integration Tests

### The look on a page
- **Intents:** [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md), [INT-0004](../../../intents/INT-0004-the-look-as-a-theme-file.md)
- `test_stone_lies_beneath_the_page`: `tests/pages/bare.html` over HTTP → the pseudo-element's image, position, layer, pointer and opacity; the body's ground.
- `test_candle_takes_its_tokens`: the same page → the glow's colour and strength are those of the tokens.
- `test_candle_is_never_stronger_than_when_still`: the stylesheet's keyframes for the candle → no step's opacity above the candle's opacity at rest.
- `test_every_bound_holds_on_the_stone_as_drawn`: a picture of that page at 1280 by 800, stillness asked → every entry of the theme file on `stone`, measured against the picture's brightest pixel, with no allowance.
- `test_plain_html_is_dressed`: `tests/pages/plain.html`, the class set → the computed font, colour and size of each plain element are the theme file's.
- `test_ornaments_are_drawn`: the same page → the clipped gradient, the seal's size, the sigil, the channel and the mark.
- `test_page_without_the_class_is_untouched`: the same page without the class, and again with no stylesheet → the same computed styles.
- `test_look_moves_unless_asked_to_be_still`: with and without reduced motion → animations running, then none.
- `test_nothing_is_in_passage_when_stillness_is_asked`: reduced motion → every element's computed transition lasts no time at all.
- `test_look_prints_plain`: print → white ground, black text, ornaments gone.
- `test_theme_changes_a_heading`: T-201, T-202 and T-205 composed, once for each of size, font, weight, slant and underline: a copy of the theme file with `h2` changed, tokens made from it by the tool → `h2` shows the change, `h1` and `h3` do not.

### The furniture on a page
- **Intents:** [INT-0006](../../../intents/INT-0006-the-furniture.md), [INT-0003](../../../intents/INT-0003-cruentous-atonement-look.md)
- `test_every_lettered_part_meets_contrast`: once for each text the list names, for each state of its part. A state at rest is found on the part's page; a state a hand brings about is brought about (the pointer moved over it, the button held down, Tab pressed to it, a rise raised from its button). The lettering's colour is read from the page and the ground behind it from a picture, by T-211's helper. An empty field's placeholder is the lettering measured there.
- `test_keyboard_reaches_and_marks_every_part_that_takes_it`: Tab through each page of parts → everything the list says takes the keyboard takes it (for a rise, the button that raises it and what is inside it once raised), each with an outline or shadow it lacks without.
- `test_controls_are_worked_by_their_keys`: Space on a tick box, arrows on a radio button, a slider and a choice → each changes.
- `test_tick_and_radio_show_their_state`: a picture of the control ticked differs from one of it unticked.
- `test_blood_carries_an_edge`: once for each part the list says the blood fills → the colour at the edge of its fill, read from a picture, against the ground beside it.
- `test_paragraph_in_every_container_is_an_inscription`: a paragraph in a plate, a panel, each kind of notice, an open fold and a shown rise → 24 pixels or more, and 3.3 or more against the ground behind it.
- `test_voids_current_row_meets_contrast`.
- `test_heading_in_a_container_is_not_carved`: an `h2` in each container → no clipped gradient, the inscription's colour, 3.3 or more against the ground behind it.
- `test_fold_opens_without_script`, `test_folds_sharing_a_name_open_one_at_a_time`, `test_rise_opens_and_closes_without_script`, `test_dialog_opens_modal_without_script`.
- `test_masthead_carries_the_briar`, `test_current_place_is_marked_beyond_colour`.
- `test_furniture_moves_unless_asked_to_be_still`, `test_no_part_is_in_passage_when_stillness_is_asked`, `test_furniture_prints_plain`: on `tests/pages/every-part.html`.
- Every page under `tests/pages/` is opened with script off.

### The release and the site
- **Intents:** [INT-0005](../../../intents/INT-0005-versioned-releases.md), [INT-0007](../../../intents/INT-0007-the-showroom.md)
- `test_release_look_works_flat`: a bundle in a temporary folder, a page written there linking the four files by bare name → fonts load, the ground is the look's.
- `test_fetch_release_matches_repository`: the example fetches a served bundle → the fonts' files, the licences and the look's four are the repository's (Sprint 0's test, extended).
- `test_site_is_built_whole`: `tools/build-site.sh` → the folder's listing.

## End-to-End Tests
- **Status:** possible, for everything but the two checks named at the end of this section
- `test_showroom_loads_from_the_kit_alone`: the showroom over HTTP from a copy of the repository → every face it uses loaded, no failed request, no request to another host. Passes only if all three hold.
- `test_showroom_shows_every_part_in_every_resting_state`: every part of the list, in each state the list gives it at rest, is on the page and visible.
- `test_showroom_imitates_no_state`: `showroom.css` → no rule on a `cruor-` class, no `:hover`, `:active`, `:focus` or `:checked`.
- `test_showroom_gives_each_parts_html`, `test_a_parts_html_draws_the_part`: the HTML beside each part, set alone in a page with the kit linked, draws a part of the same computed size and colours.
- `test_showroom_links_only_the_kit`, `test_showroom_stylesheet_adds_no_colour`.
- `test_showroom_stands_without_script`: script off → every part visible.
- `test_showroom_sets_the_fixed_pitch_families_side_by_side`: one line in each fixed-pitch family of `fonts/families.toml`, each loaded and named.
- `test_plaything_pours_and_pools`, `test_plaything_is_still_when_asked`, `test_copy_gives_the_parts_html`: script on.
- `test_showroom_loads_from_the_site`: the showroom opened from the folder `tools/build-site.sh` makes, as GitHub Pages would serve it → every face loaded, no failed request.
- **Not yet possible:** the showroom at its address on the web, unlocked when the owner turns GitHub Pages on and sets the repository variable, under [INT-0007](../../../intents/INT-0007-the-showroom.md) criterion 1 and carried past the sprint by backlog task T-104; and a fetch of the look from a published release, unlocked by the first version tag, under [INT-0005](../../../intents/INT-0005-versioned-releases.md) criterion 5 and backlog task T-102.

## By review
- `review_own_terms_before_each_push`: the entries of `own-terms-review.md` (T-216).
- `review_default_branch_holds_the_fonts`: the listing of the default branch on GitHub, recorded in INT-0002, and INT-0001 criterion 1 recorded as true of it (T-215).
- `review_owner_sees_the_showroom`: when the showroom first stands, the owner is shown it and says four things: whether it is a place and not a list (INT-0007 6); whether it is the same look as Tome's, in Cruor (INT-0003 6); which family sets code, from the side by side; and whether the foot of a carved heading stays as it is or is lifted (INT-0003 3). The answers are recorded in the test report and in INT-0003, and the later tasks wait for them (T-209).
