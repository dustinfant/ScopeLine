class FindingStore:
    def __init__(self):
        self._findings = []

    def add(self, finding: dict):
        """
        Add a normalized finding object.
        """
        self._findings.append(finding)

    def __iter__(self):
        """
        Allows: for f in ctx.findings
        """
        return iter(self._findings)

    def __len__(self):
        return len(self._findings)

    def all(self):
        """
        Explicit accessor if needed by reporters.
        """
        return self._findings

