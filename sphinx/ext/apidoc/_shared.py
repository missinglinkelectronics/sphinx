from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from sphinx.locale import __
from sphinx.util import logging

if TYPE_CHECKING:
    from collections.abc import Sequence, Set
    from pathlib import Path
    from typing import Final, Self

    from sphinx.config import Config

LOGGER: Final[logging.SphinxLoggerAdapter] = logging.getLogger('sphinx.ext.apidoc')


def _remove_old_files(
    written_files: Sequence[Path], dest_dir: Path, suffix: str
) -> None:
    files_to_keep = frozenset(written_files)
    for existing in dest_dir.rglob(f'*.{suffix}'):
        if existing not in files_to_keep:
            try:
                existing.unlink()
            except OSError as exc:
                LOGGER.warning(
                    __('Failed to remove %s: %s'),
                    existing,
                    exc.strerror,
                    type='autodoc',
                )


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ApidocOptions:
    """Options for apidoc."""

    dest_dir: Path
    module_path: Path

    exclude_pattern: Sequence[str] = ()
    max_depth: int = 4
    follow_links: bool = False
    separate_modules: bool = False
    include_private: bool = False
    toc_file: str = 'modules'
    no_headings: bool = False
    module_first: bool = False
    implicit_namespaces: bool = False
    automodule_options: Set[str] = dataclasses.field(default_factory=set)
    suffix: str = 'rst'

    remove_old: bool = True

    quiet: bool = False
    dry_run: bool = False
    force: bool = True

    # --full only
    full: bool = False
    append_syspath: bool = False
    header: str = ''
    author: str | None = None
    version: str | None = None
    release: str | None = None
    extensions: Sequence[str] | None = None
    template_dir: str | None = None


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ApidocDefaults:
    """Default values for apidoc options."""

    exclude_patterns: list[str]
    automodule_options: frozenset[str]
    max_depth: int
    follow_links: bool
    separate_modules: bool
    include_private: bool
    no_headings: bool
    module_first: bool
    implicit_namespaces: bool

    @classmethod
    def from_config(cls, config: Config, /) -> Self:
        """Collect the default values for apidoc options."""
        return cls(
            exclude_patterns=config.apidoc_exclude_patterns,
            automodule_options=frozenset(config.apidoc_automodule_options),
            max_depth=config.apidoc_max_depth,
            follow_links=config.apidoc_follow_links,
            separate_modules=config.apidoc_separate_modules,
            include_private=config.apidoc_include_private,
            no_headings=config.apidoc_no_headings,
            module_first=config.apidoc_module_first,
            implicit_namespaces=config.apidoc_implicit_namespaces,
        )
