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
          <a href={parent.href}>{parent.displayName}</a>
        </li>
      ))}
      <li className="breadcrumb-item active" aria-current="page">
        {currentPage}
      </li>
    </ol>
  </nav>
);
