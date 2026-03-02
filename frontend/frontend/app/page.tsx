import { Companies } from "./components/companies";
import Filters from "./components/filters";


export default function Home() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-6">
      <Companies filters={<Filters />} />
    </div>
  );
}
