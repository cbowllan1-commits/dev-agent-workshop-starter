import type { Stats } from "../types";

interface StatsBarProps {
  stats: Stats | null;
}

export default function StatsBar({ stats }: StatsBarProps) {
  if (!stats) return null;

  const cards = [
    { label: "Total Products", value: stats.total, color: "bg-blue-500" },
    { label: "In Stock", value: stats.in_stock, color: "bg-green-500" },
    { label: "Low Stock", value: stats.low_stock, color: "bg-yellow-500" },
    { label: "Out of Stock", value: stats.out_of_stock, color: "bg-red-500" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {cards.map((card) => (
        <div
          key={card.label}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-4"
        >
          <div className="flex items-center">
            <div className={`w-3 h-3 rounded-full ${card.color} mr-3`} />
            <div>
              <p className="text-sm text-gray-500">{card.label}</p>
              <p className="text-2xl font-semibold text-gray-900">
                {card.value}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
