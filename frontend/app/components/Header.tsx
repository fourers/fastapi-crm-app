import { Link } from "react-router-dom";

import { type HeaderPath } from "~/utils/breadcrumbs";

interface HeaderProps {
  parents: HeaderPath[];
  currentPage: string;
}

export const Header = ({ parents, currentPage }: HeaderProps) => (
  <nav aria-label="breadcrumb" className="mb-4">
    <ol className="breadcrumb">
      {parents.map((parent) => (
        <li className="breadcrumb-item">
          <Link to={parent.href}>{parent.displayName}</Link>
        </li>
      ))}
      <li className="breadcrumb-item active" aria-current="page">
        {currentPage}
      </li>
    </ol>
  </nav>
);
