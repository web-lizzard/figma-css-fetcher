from fetch_data import fetch_data
from scipy.spatial import KDTree
from webcolors import (
    hex_to_rgb,
)

names_to_hex = {
    "SLATE_050": "#f8fafc",
    "SLATE_100": "#f1f5f9",
    "SLATE_200": "#e2e8f0",
    "SLATE_300": "#cbd5e1",
    "SLATE_400": "#94a3b8",
    "SLATE_500": "#64748b",
    "SLATE_600": "#475569",
    "SLATE_700": "#334155",
    "SLATE_800": "#1e293b",
    "SLATE_900": "#0f172a",
    "GRAY_050": "#f9fafb",
    "GRAY_100": "#f3f4f6",
    "GRAY_200": "#e5e7eb",
    "GRAY_300": "#d1d5db",
    "GRAY_400": "#9ca3af",
    "GRAY_500": "#6b7280",
    "GRAY_600": "#4b5563",
    "GRAY_700": "#374151",
    "GRAY_800": "#1f2937",
    "GRAY_900": "#111827",
    "ZINC_050": "#fafafa",
    "ZINC_100": "#f4f4f5",
    "ZINC_200": "#e4e4e7",
    "ZINC_300": "#d4d4d8",
    "ZINC_400": "#a1a1aa",
    "ZINC_500": "#71717a",
    "ZINC_600": "#52525b",
    "ZINC_700": "#3f3f46",
    "ZINC_800": "#27272a",
    "ZINC_900": "#18181b",
    "NEUTRAL_050": "#fafafa",
    "NEUTRAL_100": "#f5f5f5",
    "NEUTRAL_200": "#e5e5e5",
    "NEUTRAL_300": "#d4d4d4",
    "NEUTRAL_400": "#a3a3a3",
    "NEUTRAL_500": "#737373",
    "NEUTRAL_600": "#525252",
    "NEUTRAL_700": "#404040",
    "NEUTRAL_800": "#262626",
    "NEUTRAL_900": "#171717",
    "STONE_050": "#fafaf9",
    "STONE_100": "#f5f5f4",
    "STONE_200": "#e7e5e4",
    "STONE_300": "#d6d3d1",
    "STONE_400": "#a8a29e",
    "STONE_500": "#78716c",
    "STONE_600": "#57534e",
    "STONE_700": "#44403c",
    "STONE_800": "#292524",
    "STONE_900": "#1c1917",
    "RED_050": "#fef2f2",
    "RED_100": "#fee2e2",
    "RED_200": "#fecaca",
    "RED_300": "#fca5a5",
    "RED_400": "#f87171",
    "RED_500": "#ef4444",
    "RED_600": "#dc2626",
    "RED_700": "#b91c1c",
    "RED_800": "#991b1b",
    "RED_900": "#7f1d1d",
    "ORANGE_050": "#fff7ed",
    "ORANGE_100": "#ffedd5",
    "ORANGE_200": "#fed7aa",
    "ORANGE_300": "#fdba74",
    "ORANGE_400": "#fb923c",
    "ORANGE_500": "#f97316",
    "ORANGE_600": "#ea580c",
    "ORANGE_700": "#c2410c",
    "ORANGE_800": "#9a3412",
    "ORANGE_900": "#7c2d12",
    "AMBER_050": "#fffbeb",
    "AMBER_100": "#fef3c7",
    "AMBER_200": "#fde68a",
    "AMBER_300": "#fcd34d",
    "AMBER_400": "#fbbf24",
    "AMBER_500": "#f59e0b",
    "AMBER_600": "#d97706",
    "AMBER_700": "#b45309",
    "AMBER_800": "#92400e",
    "AMBER_900": "#78350f",
    "YELLOW_050": "#fefce8",
    "YELLOW_100": "#fef9c3",
    "YELLOW_200": "#fef08a",
    "YELLOW_300": "#fde047",
    "YELLOW_400": "#facc15",
    "YELLOW_500": "#eab308",
    "YELLOW_600": "#ca8a04",
    "YELLOW_700": "#a16207",
    "YELLOW_800": "#854d0e",
    "YELLOW_900": "#713f12",
    "LIME_050": "#f7fee7",
    "LIME_100": "#ecfccb",
    "LIME_200": "#d9f99d",
    "LIME_300": "#bef264",
    "LIME_400": "#a3e635",
    "LIME_500": "#84cc16",
    "LIME_600": "#65a30d",
    "LIME_700": "#4d7c0f",
    "LIME_800": "#3f6212",
    "LIME_900": "#365314",
    "EMERALD_050": "#ecfdf5",
    "EMERALD_100": "#d1fae5",
    "EMERALD_200": "#a7f3d0",
    "EMERALD_300": "#6ee7b7",
    "EMERALD_400": "#34d399",
    "EMERALD_500": "#10b981",
    "EMERALD_600": "#059669",
    "EMERALD_700": "#047857",
    "EMERALD_800": "#065f46",
    "EMERALD_900": "#064e3b",
    "TEAL_050": "#f0fdfa",
    "TEAL_100": "#ccfbf1",
    "TEAL_200": "#99f6e4",
    "TEAL_300": "#5eead4",
    "TEAL_400": "#2dd4bf",
    "TEAL_500": "#14b8a6",
    "TEAL_600": "#0d9488",
    "TEAL_700": "#0f766e",
    "TEAL_800": "#115e59",
    "TEAL_900": "#134e4a",
    "CYAN_050": "#ecfeff",
    "CYAN_100": "#cffafe",
    "CYAN_200": "#a5f3fc",
    "CYAN_300": "#67e8f9",
    "CYAN_400": "#22d3ee",
    "CYAN_500": "#06b6d4",
    "CYAN_600": "#0891b2",
    "CYAN_700": "#0e7490",
    "CYAN_800": "#155e75",
    "CYAN_900": "#164e63",
    "SKY_050": "#f0f9ff",
    "SKY_100": "#e0f2fe",
    "SKY_200": "#bae6fd",
    "SKY_300": "#7dd3fc",
    "SKY_400": "#38bdf8",
    "SKY_500": "#0ea5e9",
    "SKY_600": "#0284c7",
    "SKY_700": "#0369a1",
    "SKY_800": "#075985",
    "SKY_900": "#0c4a6e",
    "BLUE_050": "#eff6ff",
    "BLUE_100": "#dbeafe",
    "BLUE_200": "#bfdbfe",
    "BLUE_300": "#93c5fd",
    "BLUE_400": "#60a5fa",
    "BLUE_500": "#3b82f6",
    "BLUE_600": "#2563eb",
    "BLUE_700": "#1d4ed8",
    "BLUE_800": "#1e40af",
    "BLUE_900": "#1e3a8a",
    "INDIGO_050": "#eef2ff",
    "INDIGO_100": "#e0e7ff",
    "INDIGO_200": "#c7d2fe",
    "INDIGO_300": "#a5b4fc",
    "INDIGO_400": "#818cf8",
    "INDIGO_500": "#6366f1",
    "INDIGO_600": "#4f46e5",
    "INDIGO_700": "#4338ca",
    "INDIGO_800": "#3730a3",
    "INDIGO_900": "#312e81",
    "VIOLET_050": "#f5f3ff",
    "VIOLET_100": "#ede9fe",
    "VIOLET_200": "#ddd6fe",
    "VIOLET_300": "#c4b5fd",
    "VIOLET_400": "#a78bfa",
    "VIOLET_500": "#8b5cf6",
    "VIOLET_600": "#7c3aed",
    "VIOLET_700": "#6d28d9",
    "VIOLET_800": "#5b21b6",
    "VIOLET_900": "#4c1d95",
    "PURPLE_050": "#faf5ff",
    "PURPLE_100": "#f3e8ff",
    "PURPLE_200": "#e9d5ff",
    "PURPLE_300": "#d8b4fe",
    "PURPLE_400": "#c084fc",
    "PURPLE_500": "#a855f7",
    "PURPLE_600": "#9333ea",
    "PURPLE_700": "#7e22ce",
    "PURPLE_800": "#6b21a8",
    "PURPLE_900": "#581c87",
    "FUCHSIA_050": "#fdf4ff",
    "FUCHSIA_100": "#fae8ff",
    "FUCHSIA_200": "#f5d0fe",
    "FUCHSIA_300": "#f0abfc",
    "FUCHSIA_400": "#e879f9",
    "FUCHSIA_500": "#d946ef",
    "FUCHSIA_600": "#c026d3",
    "FUCHSIA_700": "#a21caf",
    "FUCHSIA_800": "#86198f",
    "FUCHSIA_900": "#701a75",
    "PINK_050": "#fdf2f8",
    "PINK_100": "#fce7f3",
    "PINK_200": "#fbcfe8",
    "PINK_300": "#f9a8d4",
    "PINK_400": "#f472b6",
    "PINK_500": "#ec4899",
    "PINK_600": "#db2777",
    "PINK_700": "#be185d",
    "PINK_800": "#9d174d",
    "PINK_900": "#831843",
    "ROSE_050": "#fff1f2",
    "ROSE_100": "#ffe4e6",
    "ROSE_200": "#fecdd3",
    "ROSE_300": "#fda4af",
    "ROSE_400": "#fb7185",
    "ROSE_500": "#f43f5e",
    "ROSE_600": "#e11d48",
    "ROSE_700": "#be123c",
    "ROSE_800": "#9f1239",
    "ROSE_900": "#881337",
}


def convert_rgb_to_names(rgb: tuple) -> str:
    differences = {}
    for color_name, color_hex in names_to_hex.items():
        r, g, b = hex_to_rgb(color_hex)
        differences[
            sum([(r - rgb[0]) ** 2, (g - rgb[1]) ** 2, (b - rgb[2]) ** 2])
        ] = color_name
    return differences[min(differences.keys())]


class Scraper:
    def __init__(self):
        self.font_families = set()
        self.font_weights = set()
        self.font_sizes = set()
        self.letter_spacing = set()
        self.colors_set = set()
        self.shadows = []
        self.colors = []

        self.scrap_values_from_figma(fetch_data())
        for color in self.colors_set:
            self.append_new_color(color)

    def scrap_values_from_figma(self, children):

        for child in children:
            nodes = child.get("children")

            colors = child.get("backgroundColor")
            type_style = child.get("style")
            effects = child.get("effects")

            if colors:
                self.set_colors(colors)

            if type_style:
                self.set_fonts(type_style)

            if effects:
                self.set_shadows(effects)

            if nodes and len(nodes):
                self.scrap_values_from_figma(nodes)

    def set_colors(self, colors):
        color = tuple((round(colors[hue] * 255)) for hue in colors)
        self.colors_set.add(color)

    def set_fonts(self, fonts):
        self.font_families.add(fonts["fontFamily"])
        self.font_weights.add(fonts["fontWeight"])
        self.letter_spacing.add(round(fonts["letterSpacing"], 2))
        self.font_sizes.add(round(fonts["fontSize"]))

    def set_shadows(self, effects):
        for effect in effects:
            pass

    def append_new_color(self, color: dict):
        self.colors.append(
            {
                "name": convert_rgb_to_names((color[0], color[1], color[2])),
                "color": color,
            }
        )
