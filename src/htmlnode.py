from functools import reduce


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict[str, str] = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return (
            reduce(
                lambda html, item: f'{html} {item[0]}="{item[1]}"',
                self.props.items(),
                "",
            )
            if self.props
            else ""
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All LeafNodes must have a value.")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All ParentNodes must have a tag.")

        if not self.children or len(self.children) == 0:
            raise ValueError("All ParentNodes must have children.")

        return f"<{self.tag}{self.props_to_html()}>{reduce(lambda html, child: html + child.to_html(), self.children, '')}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, value={self.value}, childeren={self.children if len(self.children) <= 3 else len(self.children)}, props={self.props})"
