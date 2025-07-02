from dataclasses import dataclass


@dataclass(kw_only=True)
class MWebInternalConfig:
    staticUrlPath: str | None = None
    staticFolder: str | None = "static"
    staticHost: str | None = None
    hostMatching: bool = False
    subdomainMatching: bool = False
    templateFolder: str | None = "templates"
    instancePath: str | None = None
    instanceRelativeConfig: bool = False
    rootPath: str | None = None


@dataclass(kw_only=True)
class MWebModuleDetails:
    systemName: str  # Should be alphabet then number with - (hyphen)
    displayName: str = None
