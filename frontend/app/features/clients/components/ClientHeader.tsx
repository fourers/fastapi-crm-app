interface ClientHeaderProps {
  sectionName: string;
}

export const ClientHeader = ({ sectionName }: ClientHeaderProps) => (
  <nav aria-label="breadcrumb" className="mb-4">
    <ol className="breadcrumb">
      <li className="breadcrumb-item">
        <a href="/clients">Clients</a>
      </li>
      <li className="breadcrumb-item active" aria-current="page">
        {sectionName}
      </li>
    </ol>
  </nav>
);
