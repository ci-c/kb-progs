import pathlib
from abc import ABC, abstractmethod


class IKnowlageBaseBlock(ABC):
    @abstractmethod
    def get_body(self) -> str:
        pass

    @abstractmethod
    def get_childrens(self) -> list["KnowlageBaseBlock"]:
        pass

    @abstractmethod
    def add_child(self, child: "KnowlageBaseBlock") -> None:
        pass

    @abstractmethod
    def del_child(self, child: "KnowlageBaseBlock") -> None:
        pass

    @abstractmethod
    def get_path(self) -> pathlib.Path:
        pass

    @abstractmethod
    def get_parent(self) -> "KnowlageBaseBlock" | None:
        pass

    @abstractmethod
    def get_links(self) -> list["KnowlageBaseBlock"]:
        pass

    @abstractmethod
    def get_backlinks(self) -> list["KnowlageBaseBlock"]:
        pass

    @abstractmethod
    def set_body(self, body: str) -> None:
        pass


class KnowlageBaseBlock(IKnowlageBaseBlock, ABC):
    pass

class KnowlageBaseStrBlock(IKnowlageBaseBlock):
    pass


class KnowlageBaseFolderBlock(IKnowlageBaseBlock):
    def __init__(self, path: pathlib.Path):
        self.__body = ""
        self.__childrens = [
            KnowlageBaseBlockFactory.create_block(i) for i in path.iterdir()]


class KnowlageBaseFileBlock(IKnowlageBaseBlock):
    def __init__(self, path: pathlib.Path):
        self.__body = ""
        # TODO: read and parse file


class KnowlageBaseBlockFactory:
    @staticmethod
    def create_block(raw: pathlib.Path | str) -> KnowlageBaseBlock:
        if type(raw) is pathlib.Path:
            if raw.is_dir():
                return KnowlageBaseFolderBlock(raw)
            elif raw.is_file():
                return KnowlageBaseFileBlock(raw)
            else:
                raise ValueError("Path is not a file or directory")
        elif type(raw) is str:
            return KnowlageBaseStrBlock(raw)
    
    @staticmethod
    def create_block_from_str(string: str) -> KnowlageBaseBlock:
        pass



