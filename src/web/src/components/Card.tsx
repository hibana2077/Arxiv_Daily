export function PaperCard({ title, content, link }:{ title: string, content: string, link: string}) {
  return (
    <div className="divide-y divide-gray-200 overflow-hidden rounded-lg bg-white shadow">
      <div className="px-4 py-5 sm:px-6">
        {title}
      </div>
      <div className="px-4 py-5 sm:p-6">{content}</div>
      <div className="px-4 py-4 sm:px-6">
        {link}
      </div>
    </div>
  );
}