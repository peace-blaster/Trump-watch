# Trump watch

A small Linux command-line app for Donald Trump's published job-approval polling. It reads **YouGov's second-term tracker, US Registered Voters**, showing approval, disapproval, not sure, source tracker dates and unweighted sample bases. It covers one source and one population, not all polls. It does not calculate averages, scores, rankings, forecasts or political assessments.

## Requirements

Python **3.8 or newer**, including the standard `ssl`, `zlib`, XML and urllib modules; trusted system CA certificates; and HTTPS/DNS access to YouGov for refreshes. No pip packages, API keys, account, Excel, curl, root access or background service are needed. Install/uninstall use POSIX `/bin/sh` and ordinary Linux utilities. Python is widely available but is not guaranteed on minimal distributions; install Python 3 and CA certificates through your distribution's package manager if absent. Architecture independent; tested on this Linux host, not every distribution.

## Run and install

From the extracted directory:

```sh
./trump-watch
./install.sh
~/.local/bin/trump-watch --history 5
```

Default install location is `~/.local/bin/trump-watch`. Add `~/.local/bin` to your shell's PATH if necessary. Or choose a writable prefix: `./install.sh /your/prefix`. The installer refuses existing files; uninstall before upgrading. You can also run `python3 ./trump-watch` without installation.

```sh
trump-watch --history 12   # last 12 available source dates
trump-watch --offline     # last successful download, no network
trump-watch --json        # data plus attribution/status as JSON
trump-watch --cache-dir /your/cache --history 5
trump-watch --help
```

Each ordinary invocation refreshes once, with a 30-second socket timeout. There is no automatic polling schedule. A valid download is atomically cached in `${XDG_CACHE_HOME:-$HOME/.cache}/trump-watch/polls.xlsx`. History is the series supplied in the latest workbook, not a permanent archive of revisions; a successful refresh replaces the cache. Cache retrieval time is recorded by the file's modification time, so externally copying/touching it can change that time.

A failed refresh uses the last valid cache with an explicit warning and exit status **2**. No usable data produces an error and exit **1**. Successful live or explicitly offline reads exit **0** (as does a successful live read whose cache could not be saved, with a warning). Argument errors exit **2**. JSON includes cache status and warnings; errors also go to stderr. Older-than-14-day source dates are labeled stale, even after a successful download. This threshold is a freshness cue, not a statistical judgment or a guarantee newer polls do not exist elsewhere.

## Source and interpretation

- [YouGov public tracker](https://yougov.com/en-us/trackers/donald-trump-approval)
- [YouGov downloadable crosstabs](https://api-test.yougov.com/public-data/v5/us/trackers/donald-trump-approval/download/)
- [YouGov methodology](https://yougov.com/about/panel-methodology)

The endpoint was discovered from the tracker page's Download crosstabs link and verified live on September 7, 2026. Despite a page-state field named `csvDownloadUrl`, it returns an XLSX workbook. The CLI reads the named `US Registered Voters` sheet using standard-library ZIP/XML support. It uses the workbook's published proportions, converted to percentages, not the website's smoothed chart. Published rounding can make responses total 99% or 101%.

The date column is explicitly the **source tracker date**. Full polling fieldwork start/end intervals, margin of error, and per-wave methodology are not supplied in this workbook and are not inferred. Consult the linked source and its poll releases for those details. Registered-voter figures should not be treated as all-adult figures. The JSON `base` field preserves the workbook's separate `Base` row; the text display uses `Unweighted base`.

The app verifies the question, population, labels, dates, percentage ranges and sample bases. It fails honestly if the source schema changes. The public website endpoint is not a guaranteed stable API. No current polling dataset is bundled; first use needs a successful network connection. YouGov owns its polling data; consult its public-data licence and terms on the source website for reuse. The app is independent of YouGov and any political campaign.

## Uninstall

```sh
./uninstall.sh                 # default prefix
./uninstall.sh /your/prefix    # same prefix used to install
```

This removes only the recognized executable and retains cache data. To remove the default cache too:

```sh
rm -f -- "${XDG_CACHE_HOME:-$HOME/.cache}/trump-watch/polls.xlsx"
rmdir -- "${XDG_CACHE_HOME:-$HOME/.cache}/trump-watch"
```

For a custom `--cache-dir`, remove its `polls.xlsx` yourself. The source directory can be deleted after uninstalling.

## Verification

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic workbook fixtures, never fabricated live polling data. See `VERIFICATION.md` for the completed live and installation checks.
