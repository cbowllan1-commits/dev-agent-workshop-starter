interface CategoryFilterProps {
  value: string;
  onChange: (category: string) => void;
}

const categories = ["All", "Electronics", "Software", "Hardware", "Accessories"];

export default function CategoryFilter({
  value,
  onChange,
}: CategoryFilterProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white"
    >
      {categories.map((cat) => (
        <option key={cat} value={cat === "All" ? "" : cat}>
          {cat}
        </option>
      ))}
    </select>
  );
}
