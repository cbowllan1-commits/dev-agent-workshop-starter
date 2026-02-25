import { useCallback, useEffect, useState } from "react";
import { deleteProduct, fetchProducts, fetchStats } from "./api/client";
import CategoryFilter from "./components/CategoryFilter";
import Header from "./components/Header";
import ProductTable from "./components/ProductTable";
import SearchBar from "./components/SearchBar";
import StatsBar from "./components/StatsBar";
import type { Product, Stats } from "./types";

export default function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [category, setCategory] = useState("");
  const [search, setSearch] = useState("");

  const loadData = useCallback(async () => {
    const [productsData, statsData] = await Promise.all([
      fetchProducts({
        category: category || undefined,
        search: search || undefined,
      }),
      fetchStats(),
    ]);
    setProducts(productsData);
    setStats(statsData);
  }, [category, search]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleDelete = async (id: string) => {
    await deleteProduct(id);
    loadData();
  };

  const handleSearch = useCallback((query: string) => {
    setSearch(query);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <StatsBar stats={stats} />
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <SearchBar onSearch={handleSearch} />
          <CategoryFilter value={category} onChange={setCategory} />
        </div>
        <ProductTable products={products} onDelete={handleDelete} />
      </main>
    </div>
  );
}
