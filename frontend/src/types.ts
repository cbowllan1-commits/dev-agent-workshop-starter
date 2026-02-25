export interface Product {
  id: string;
  name: string;
  category: "Electronics" | "Software" | "Hardware" | "Accessories";
  price: number;
  stock: number;
  sku: string;
  status: "In Stock" | "Low Stock" | "Out of Stock";
  created_at: string;
  updated_at: string;
}

export interface Stats {
  total: number;
  in_stock: number;
  low_stock: number;
  out_of_stock: number;
}
