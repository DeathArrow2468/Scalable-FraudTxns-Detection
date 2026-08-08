from copy import deepcopy
from uuid import uuid4

from utils.models import Document
from utils.chunk_models import Chunk, ChunkCollection, ChunkMetadata
from utils.heading_detector import HeadingDetector
from utils.hierarchy_builder import HierarchyBuilder


class Chunker:

    @staticmethod
    def chunk(document: Document) -> ChunkCollection:

        builder = HierarchyBuilder()

        chunks = []

        current_lines = []

        current_hierarchy = None

        chunk_index = 0

        page_start = 1
        page_end = 1

        for page in document.pages:

            page_end = page.page_number

            lines = [
                line.strip()
                for line in page.text.splitlines()
                if line.strip()
            ]

            i = 0

            while i < len(lines):

                heading = HeadingDetector.detect(lines, i)

                if heading:

                    # -----------------------------
                    # Save previous chunk
                    # -----------------------------

                    if current_lines and current_hierarchy:

                        chunks.append(
                            Chunker._create_chunk(
                                document=document,
                                hierarchy=current_hierarchy,
                                lines=current_lines,
                                chunk_index=chunk_index,
                                page_start=page_start,
                                page_end=page_end
                            )
                        )

                        chunk_index += 1

                    # -----------------------------
                    # Update hierarchy
                    # -----------------------------

                    builder.update(heading)

                    current_hierarchy = deepcopy(builder.snapshot())

                    page_start = page.page_number

                    current_lines = []

                    # -----------------------------
                    # Add hierarchy to chunk
                    # -----------------------------

                    if current_hierarchy.chapter:

                        current_lines.append(
                            f"{current_hierarchy.chapter}"
                        )

                    if current_hierarchy.chapter_title:

                        current_lines.append(
                            current_hierarchy.chapter_title
                        )

                    if current_hierarchy.section:

                        current_lines.append(
                            f"Section {current_hierarchy.section}"
                        )

                    if current_hierarchy.section_title:

                        current_lines.append(
                            current_hierarchy.section_title
                        )

                    if current_hierarchy.subsection:

                        current_lines.append(
                            f"Subsection {current_hierarchy.subsection}"
                        )

                    if current_hierarchy.subsection_title:

                        current_lines.append(
                            current_hierarchy.subsection_title
                        )

                    if current_hierarchy.subsubsection:

                        current_lines.append(
                            f"Subsection {current_hierarchy.subsubsection}"
                        )

                    if current_hierarchy.subsubsection_title:

                        current_lines.append(
                            current_hierarchy.subsubsection_title
                        )

                    # RBI headings occupy two lines
                    if heading.type != "generic" and heading.title:
                        i += 2
                    else:
                        i += 1

                    continue

                current_lines.append(lines[i])

                i += 1

        # ----------------------------------------
        # Save final chunk
        # ----------------------------------------

        if current_lines:

            if current_hierarchy is None:

                builder.current.chapter = "DOCUMENT"
                builder.current.chapter_title = document.metadata.title

                current_hierarchy = builder.snapshot()

            chunks.append(
                Chunker._create_chunk(
                    document=document,
                    hierarchy=current_hierarchy,
                    lines=current_lines,
                    chunk_index=chunk_index,
                    page_start=page_start,
                    page_end=page_end
                )
            )

        return ChunkCollection(
            document_uuid=document.metadata.document_uuid,
            chunks=chunks
        )

    @staticmethod
    def _create_chunk(
        document,
        hierarchy,
        lines,
        chunk_index,
        page_start,
        page_end
    ):

        metadata = ChunkMetadata(

            chunk_uuid=str(uuid4()),

            document_uuid=document.metadata.document_uuid,

            chunk_index=chunk_index,

            authority=document.metadata.authority,

            document_title=document.metadata.title,

            chapter=hierarchy.chapter,

            chapter_title=hierarchy.chapter_title,

            section=hierarchy.section,

            subsection=hierarchy.subsection,

            heading=(
                hierarchy.subsubsection_title
                or hierarchy.subsection_title
                or hierarchy.section_title
                or hierarchy.chapter_title
            ),

            page_start=page_start,

            page_end=page_end

        )

        return Chunk(
            metadata=metadata,
            text="\n".join(lines)
        )